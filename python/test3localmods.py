from ml_metadata.metadata_store import metadata_store
from ml_metadata.proto import metadata_store_pb2
from faker import Faker
fake = Faker()

def create_store():
    client_connection_config = metadata_store_pb2.MetadataStoreClientConfig()
    client_connection_config.host = 'localhost'
    client_connection_config.port = 8080

    store = metadata_store.MetadataStore(client_connection_config)
    return store

def create_ctx_type(store):
    experiment_type = metadata_store_pb2.ContextType()
    experiment_type.name = "Experiment"
    experiment_type.properties["note"] = metadata_store_pb2.STRING
    experiment_type_id = store.put_context_type(experiment_type)
    results = store.get_context_types()
    print(results)
    return experiment_type_id

def working(experiment_type_id):
    my_experiment = metadata_store_pb2.Context()
    my_experiment.type_id = experiment_type_id
    my_experiment.name = "exp1"
    my_experiment.properties["note"].string_value = "My first experiment."
    [experiment_id] = store.put_contexts([my_experiment])
    print(experiment_id)
    result = store.get_contexts_by_id([experiment_id])
    print(result)

def lorem(max_chars):
    result = ""
    while len(result) < max_chars:
        result += fake.sentence() + " "
    return result[:max_chars]

def not_working(experiment_type_id):
    my_experiment = metadata_store_pb2.Context()
    my_experiment.type_id = experiment_type_id
    my_experiment.name = "exp_longnote"
    my_experiment.properties["note"].string_value = lorem(2690) # up to ~2680 works
    [experiment_id] = store.put_contexts([my_experiment])
    print(experiment_id)
    result = store.get_contexts_by_id([experiment_id])
    print(result)

if __name__ == '__main__':
    store = create_store()
    experiment_type_id = create_ctx_type(store)
    working(experiment_type_id)
    not_working(experiment_type_id)
