"""
Tester service for identifying if env is blue or green.
"""
import os
import boto3
from dotenv import load_dotenv
from flask import Flask

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

def get_cluster_name(host_name):
    """
    Given the node host, retrieve the name of the cluster the pod is running on.
    """
    response = ec2.describe_instances(
        Filters=[
            {
                'Name':'private-dns-name',
                'Values': [
                    host_name
                ]
            }
        ]
    )

    tags = response['Reservations'][0]['Instances'][0]['Tags']
    for tag in tags:
        if tag['Key'] == "eks:cluster-name":
            return tag['Value']
    return ''


@app.route("/flask-service")
def blue_or_green():
    """
    This function returns if the service is running on blue or green cluster env.
    """
    cluster_name = get_cluster_name(node_name)
    return "Serving on pod: "+pod_name+" on node: "+node_name+" in the cluster: "+cluster_name

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(debug=True,host='0.0.0.0',port=port)
