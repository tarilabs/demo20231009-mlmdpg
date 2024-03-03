# Evaluate PostgreSQL Server as backend to use with ml-metadata #65

## Test 1: ml-metadata Python to PostgreSQL

Using podman compose, and `test1.py` outputs:

```
demo20231009-mlmdpg % docker exec -it e8ff94c9fc07 bash
(app-root) bash-4.4$ python test1.py 
WARNING: Logging before InitGoogleLogging() is written to STDERR
I1009 09:22:11.567962     7 postgresql_metadata_source.cc:208] Connecting to database. 
I1009 09:22:11.581920     7 postgresql_metadata_source.cc:215] Connection to database succeed.
I1009 09:22:11.626552     7 postgresql_metadata_source.cc:208] Connecting to database. 
I1009 09:22:11.630167     7 postgresql_metadata_source.cc:215] Connection to database succeed.
[id: 10
name: "DataSet"
properties {
  key: "day"
  value: INT
}
properties {
  key: "split"
  value: STRING
}
, id: 11
name: "SavedModel"
properties {
  key: "name"
  value: STRING
}
properties {
  key: "version"
  value: INT
}
]
```

As expected:

![](/screenshots/Screenshot%202023-10-09%20at%2011.26.01%20(2).png)

## Test 2: ml-metadata Python to gRPC ml-metadata server to PostgreSQL

Using podman compose, and this time `test2.py` outputs:

```
demo20231009-mlmdpg % docker ps
CONTAINER ID  IMAGE                                                  COMMAND               CREATED         STATUS                   PORTS                   NAMES
759913b5e449  gcr.io/tfx-oss-public/ml_metadata_store_server:1.14.0                        2 hours ago     Up 11 seconds            0.0.0.0:8080->8080/tcp  demo20231009-mlmdpg-mlmdserver-1
2bb711a2b659  docker.io/library/demo20231009-mlmdpg-web:latest       /bin/sh -c tail -...  22 seconds ago  Up 22 seconds                                    demo20231009-mlmdpg-web-1
b1d4d814272f  docker.io/library/postgres:12                          postgres              22 seconds ago  Up 22 seconds (healthy)  0.0.0.0:5432->5432/tcp  demo20231009-mlmdpg-pgserver-1
demo20231009-mlmdpg % docker exec -it 2bb711a2b659 bash
(app-root) bash-4.4$ python test2.py 
(app-root) bash-4.4$ 
```

As expected:

![](/screenshots/Screenshot%202023-10-09%20at%2011.35.33%20(2).png)

## Conclusions

Demonstrated PostgreSQL Server as backend to use with ml-metadata, both using direct connection as well as using the gRPC ml-metadata server.

## Test 3

```
docker run --name some-postgres \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=mypsw \
-e PGUSER=postgres \
-e PGPASSWORD=mypsw \
-p 5432:5432 \
-d "postgres:12"
```

resulting in:

```
WARNING: Logging before InitGoogleLogging() is written to STDERR
I0303 16:19:42.571434 13378 postgresql_metadata_source.cc:208] Connecting to database. 
I0303 16:19:42.576880 13378 postgresql_metadata_source.cc:215] Connection to database succeed.
I0303 16:19:43.322311 13378 postgresql_metadata_source.cc:208] Connecting to database. 
I0303 16:19:43.327381 13378 postgresql_metadata_source.cc:215] Connection to database succeed.
[id: 10
name: "Experiment"
properties {
  key: "note"
  value: STRING
}
]
1
[id: 1
type_id: 10
name: "exp1"
properties {
  key: "note"
  value {
    string_value: "My first experiment."
  }
}
type: "Experiment"
create_time_since_epoch: 1709479183548
last_update_time_since_epoch: 1709479183548
]
E0303 16:19:43.555275 13378 postgresql_metadata_source.cc:128] Execution failed: ERROR:  index row size 2712 exceeds btree version 4 maximum 2704 for index "idx_context_property_string"
DETAIL:  Index row references tuple (0,2) in relation "contextproperty".
HINT:  Values larger than 1/3 of a buffer page cannot be indexed.
Consider a function index of an MD5 hash of the value, or use full text indexing.
WARNING:absl:mlmd client InternalError: PostgreSQL metadata source error: ERROR:  index row size 2712 exceeds btree version 4 maximum 2704 for index "idx_context_property_string"
DETAIL:  Index row references tuple (0,2) in relation "contextproperty".
HINT:  Values larger than 1/3 of a buffer page cannot be indexed.
Consider a function index of an MD5 hash of the value, or use full text indexing.

Traceback (most recent call last):
  File "/home/tarilabs/git/demo20231009-mlmdpg/python/test3.py", line 61, in <module>
    not_working(experiment_type_id)
  File "/home/tarilabs/git/demo20231009-mlmdpg/python/test3.py", line 52, in not_working
    [experiment_id] = store.put_contexts([my_experiment])
  File "/home/tarilabs/git/demo20231009-mlmdpg/venv/lib64/python3.10/site-packages/ml_metadata/metadata_store/metadata_store.py", line 520, in put_contexts
    self._call('PutContexts', request, response)
  File "/home/tarilabs/git/demo20231009-mlmdpg/venv/lib64/python3.10/site-packages/ml_metadata/metadata_store/metadata_store.py", line 203, in _call
    return self._call_method(method_name, request, response)
  File "/home/tarilabs/git/demo20231009-mlmdpg/venv/lib64/python3.10/site-packages/ml_metadata/metadata_store/metadata_store.py", line 224, in _call_method
    self._pywrap_cc_call(cc_method, request, response)
  File "/home/tarilabs/git/demo20231009-mlmdpg/venv/lib64/python3.10/site-packages/ml_metadata/metadata_store/metadata_store.py", line 255, in _pywrap_cc_call
    raise errors.make_exception(error_message.decode('utf-8'), status_code)
ml_metadata.errors.InternalError: PostgreSQL metadata source error: ERROR:  index row size 2712 exceeds btree version 4 maximum 2704 for index "idx_context_property_string"
DETAIL:  Index row references tuple (0,2) in relation "contextproperty".
HINT:  Values larger than 1/3 of a buffer page cannot be indexed.
Consider a function index of an MD5 hash of the value, or use full text indexing.
```