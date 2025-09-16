#!/usr/bin/env python3
"""
Create a single EC2 instance using boto3.
Replace IMAGE_ID, KEY_NAME, and optionally SECURITY_GROUP_ID before running.
Requires AWS credentials configured (env vars, shared config, or IAM role).
"""
import boto3
import sys


def main():
    region = 'us-east-1'
    image_id = 'ami-0abcdef1234567890'  # TODO: replace with a valid AMI ID
    instance_type = 't2.micro'
    key_name = 'your-key-pair-name'     # TODO: replace with your key pair name
    sg_ids = []  # e.g. ['sg-0123456789abcdef0'] or []

    ec2 = boto3.resource('ec2', region_name=region)

    try:
        instances = ec2.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=sg_ids
        )
        instance = instances[0]
        print('Launched instance, id:', instance.id)
        instance.wait_until_running()
        instance.reload()
        print('Instance is running. Public IP:', instance.public_ip_address)
    except Exception as e:
        print('Error creating instance:', e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
