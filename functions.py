import os
import boto3
from flask import flash
from botocore.exceptions import ClientError
import logging
from bson.objectid import ObjectId


def check_activity_id(activity_id):
    """Check if id is a valid objectId

    :param activity_id: string
    :return: True if the id is valid, else False and flash error
    """
    if not ObjectId.is_valid(activity_id):
        flash('Activity ID not valid', 'error')
        return False
    else:
        return True


def s3_image_exists(file_name):
    """Check if an activity has an image

    :param file_name: string
    :return: True if the image exists, else False
    """
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket_name, file_name).load()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print('File not found!')
            return False
        else:
            # Something else has gone wrong.
            print(f'System error: {e}')
            return False
    else:
        print('Found OK')
        return True


def set_imageURL(activity_id):
    """Create imageURL based on if the activity image actually exists

    :param activity_id: string or bson.objectid.ObjectId
    :return: Either presigned URL or no_image path
    """
    check_file = f'{ activity_id }.jpg'
    print(f'Does this file: {check_file} exists?')

    if s3_image_exists(check_file):
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        imageURL = create_presigned_url(bucket_name,
                                        check_file, expiration=3600)
    else:
        imageURL = '/static/images/no_image_yet.jpg'
    return imageURL


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')

    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
