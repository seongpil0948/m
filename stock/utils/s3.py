import os
import logging
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def upload_file(file_name, bucket='mmoney', object_name=None, ACL='public-read'):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    if ACL:
        ExtraArgs = {'ACL': ACL}
    else:
        ExtraArgs = {}
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=ExtraArgs)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def put_object(dest_bucket_name, dest_object_name, src_data, ACL='public-read'):
    """Add an object to an Amazon S3 bucket
    The src_data argument must be of type bytes or a string that references
    a file specification.
    :param dest_bucket_name: string
    :param dest_object_name: string
    :param src_data: bytes of data or string reference to file spec
    :return: True if src_data was added to dest_bucket/dest_object, otherwise
    False
    """

    # Construct Body= parameter
    if isinstance(src_data, bytes):
        object_data = src_data
    elif isinstance(src_data, str):
        try:
            object_data = open(src_data, 'rb')
        except Exception as e:
            logging.error(e)
            return False
    else:
        logging.error('Type of ' + str(type(src_data)) + ' for the argument \'src_data\' is not supported.')
        return False

    # Put the object
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_data, ACL=ACL)
    except ClientError as e:
        logging.error(e)
        return False
    finally:
        if isinstance(src_data, str):
            object_data.close()
    return True


def upload_fileobj(file, bucket='mmoney', object_name=None, ACL='public-read'):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if ACL:
        ExtraArgs = {'ACL': ACL}
    else:
        ExtraArgs = {}
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_fileobj(file, bucket, object_name, ExtraArgs=ExtraArgs)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def plt_upload(file, tech_name):
    """
    file: 업로드 할 이미지 파일을 넣어주시면 됩니다.
    path: 업로드 할 경로를 넣어주시면 됩니다.

    example:
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')

    tech_name = 'bollinger_band'  # 기법명
    file_name = str(uuid.uuid4())  # 파일명 임시로 uuid 로 박아둠
    path = f'media/{tech_name}/{file_name}.png'

    plt_upload(img_data, path)
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
    target = file.name.split('/')[1]
    path = f'media/{tech_name}/{target}'
    try:
        bucket.put_object(Body=file, ContentType='image/png', Key=path)
    except ClientError as e:
        logging.error(e)
        return False
    else:
        os.remove(f'media/{target}')


if __name__ == "__main__":
    """
    upload_file(file_name, bucket='mmoney', 'media/<기법>/<이미지명>)
    """
    file_name = 'media/images/text.txt'
    bucket = 'mmoney'
    object_name = 'media/test/text.txt'

    print(upload_file(file_name, bucket, object_name))
