from google.cloud import container
from kubernetes import client, config
import google.auth
import os
import logging
import datetime
from tempfile import NamedTemporaryFile
import base64
from google.cloud import datastore
logging.basicConfig(level=logging.DEBUG)


def initialize_datastore_client():
    return datastore.Client()
def write_node_to_datastore(client, node_name, node_pool, cluster_id,k8s_client):
    # Define the key for the entity using the namespace and kind
    key = client.key(data_store_kind, node_name, namespace=data_store_namespace)
    
    # Retrieve the entity if it exists
    entity = client.get(key)
    
    if entity:
        print(f"Entity exists for node {node_name}. Incrementing count.")
        # Increment the count attribute if the entity exists
        if 'count' in entity:
            entity['count'] += 1
        else:
            entity['count'] = 1  # Initialize count if not present
    else:
        print(f"Creating new entity for node {node_name}.")
        entity = datastore.Entity(key=key)
        entity['count'] = 1  # Initialize count for new entity
    if entity['count'] >= cut_off_node_count:
        message = f"Node {node_name} has no running pods for more than 6 hours , Node Pool: {node_pool} , node {node_name}is being deleted "
        k8s_client.delete_node(node_name)
    # Update or set other attributes of the entity
    entity.update({
        'node_name': node_name,
        'node_pool': node_pool,
        'cluster_id': cluster_id,
        'timestamp': datetime.datetime.utcnow()
    })
    
    # Save the entity to the datastore
    client.put(entity)
    print(f"Data for node {node_name} saved in Datastore with count {entity['count']}.")

def token_gen(*scopes):
    print('Getting Token for cluster connect')
    credentials, project = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    print("credentials token generated successfully")
    return credentials

def list_pods(request):
        # Read environment variables
    project_id = os.getenv('PROJECT_ID', 'default-project')
    zone = os.getenv('ZONE', 'default-zone')
    cluster_id = os.getenv('CLUSTER_ID', 'default-cluster')
    cut_off_node_count = os.getenv('NODE_COUNT',2)
    data_store_namespace = os.getenv('DATA_STORE_NS',"ListPods")
    data_store_kind = getenv('DATA_STORE_KIND','NodePoolName')
    exclusion_keywords = ("-ops-", "-istio-")
    datastore_client = initialize_datastore_client()
    # Create a Cluster Manager Client and get cluster credentials
    cluster_manager_client = container.ClusterManagerClient()
    cluster = cluster_manager_client.get_cluster(name=f'projects/{project_id}/locations/{zone}/clusters/{cluster_id}')
    configuration = client.Configuration()
    configuration.host = f"https://{cluster.endpoint}"
    with NamedTemporaryFile(delete=False) as ca_cert:
        ca_cert.write(base64.b64decode(cluster.master_auth.cluster_ca_certificate))
    configuration.ssl_ca_cert = ca_cert.name    
    configuration.api_key_prefix['authorization'] = 'Bearer'  
    configuration.api_key['authorization'] = token_gen().token
    client.Configuration.set_default(configuration)
    v1 = client.CoreV1Api()

    # List all nodes
    nodes = v1.list_node()
    node_names = [node.metadata.name for node in nodes.items]

    # Define namespaces to ignore if found on the node
    excluded_namespaces = {'kube-system', 'monitoring'}

    # Dictionary to hold node and running pod count
    node_pod_count = {node: 0 for node in node_names}

    # List all pods and check nodes
    pods = v1.list_pod_for_all_namespaces()
    for pod in pods.items:
        if pod.metadata.namespace not in excluded_namespaces:
            if pod.spec.node_name in node_pod_count:
                node_pod_count[pod.spec.node_name] += 1

    message=""
    # Print nodes with no running pods and their nodepool
    for node in nodes.items:
        if node_pod_count[node.metadata.name] == 0:
            pairs = node.metadata.annotations["node.gke.io/last-applied-node-labels"].split(",")
            parsed_dict = {}
            for pair in pairs:
                key, value = pair.split('=', 1)  # The '1' ensures only the first '=' is used for splitting
                parsed_dict[key] = value
            nodepool = parsed_dict.get("cloud.google.com/gke-nodepool", "Key not found")
            print(f"Node {node.metadata.name} has no running pods. Node Pool: {nodepool}")
            message = f"Node {node.metadata.name} has no running pods. Node Pool: {nodepool}"
            # ignore sepcific nodes 
            if all(keyword not in node.metadata.name for keyword in exclusion_keywords):
                write_node_to_datastore(datastore_client, node.metadata.name, nodepool, cluster_id,v1)
    return ("Function Execution Completed",200)



