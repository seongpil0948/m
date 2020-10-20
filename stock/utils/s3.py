import os
import logging
import boto3
from botocore.exceptions import ClientError


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


if __name__ == "__main__":
    """
    upload_file(file_name, bucket='mmoney', 'media/<기법>/<이미지명>)
    """
    file_name = 'media/images/text.txt'
    bucket = 'mmoney'
    object_name = 'media/test/text.txt'

    print(upload_file(file_name, bucket, object_name))
