"""
Tester service for identifying if env is blue or green.
"""
import os
import boto3
from dotenv import load_dotenv
from flask import Flask

#TODO
# 1) use boto3 to get node name based on eks tags
# 2) match the node name to the node name received from Kubernetes Downward API
# 3) if it matches the green cluster, then we are on green
# 4) if it matches the blue cluster, then we are on blue

# Cutover strategy
# blue load balancer -> blue target groups
# green load balancer -> green target groups
# main load balancer -> either blue or green target groups
# at cut over, check if green or blue, then cutover
# rollback to blue/green if required

load_dotenv()

app = Flask(__name__)

node_name = os.environ['NODE_NAME']
pod_name = os.environ['POD_NAME']

ec2 = boto3.client('ec2',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name='us-east-1'
)

def get_host_names(name):
    """
    Get all host names that are part of an eks cluster
    """
    response = ec2.describe_instances(
        Filters=[
            {
                'Name':'tag-key',
                'Values': [
                    'eks:cluster-name'
                ]
            }
        ]
    )

    reservations = response['Reservations']
    print(reservations)
    for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
            network_interfaces = instance['NetworkInterfaces']
            for network_interface in network_interfaces:
                host_names = network_interface['PrivateDnsName']
                return host_names

@app.route("/flask-service")
def blue_or_green():
    """
    This function returns if the service is running on blue or green cluster env.
    """
    get_host_names(node_name)
    return "This service is running on pod: "+pod_name+" on node: "+node_name

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(debug=True,host='0.0.0.0',port=port)
