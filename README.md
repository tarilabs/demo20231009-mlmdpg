# Evaluate PostgreSQL Server as backend to use with ml-metadata #65

# Test 1: ml-metadata Python to PostgreSQL

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

# Test 2: ml-metadata Python to gRPC ml-metadata server to PostgreSQL

todo
