

from jsonschema import validate


structure = {
    "default": {
        "ip": {
            "name": "ip地址",
            "field": "string",
            "max": 200,
            "required": True
        },
        "cpu": {
            "name": "cpu",
            "field": "string",
            "max": 200,
            "required": True
        },
        "memory": {
            "name": "内存",
            "field": "int",
            "max": 10,
            "required": True
        }
    }
}

schema = {
    "$schema": "http://json-schema.org/draft-03/schema#", 
    "required": True, 
    "type": "object", 
    "id": "#", 
    "properties": {
        "default": {
            "required": True, 
            "type": "object", 
            "id": "default", 
            "properties": {
                "ip": {
                    "required": True, 
                    "type": "object", 
                    "id": "ip", 
                    "properties": {
                        "field": {
                            "required": True, 
                            "type": "string", 
                            "id": "field"
                        }, 
                        "required": {
                            "required": True, 
                            "type": "boolean", 
                            "id": "required"
                        }, 
                        "name": {
                            "required": True, 
                            "type": "string", 
                            "id": "name"
                        }, 
                        "max": {
                            "required": True, 
                            "type": "number", 
                            "id": "max"
                        }
                    }
                }, 
                "cpu": {
                    "required": True, 
                    "type": "object", 
                    "id": "cpu", 
                    "properties": {
                        "field": {
                            "required": True, 
                            "type": "string", 
                            "id": "field"
                        }, 
                        "required": {
                            "required": True, 
                            "type": "boolean", 
                            "id": "required"
                        }, 
                        "name": {
                            "required": True, 
                            "type": "string", 
                            "id": "name"
                        }, 
                        "max": {
                            "required": True, 
                            "type": "number", 
                            "id": "max"
                        }
                    }
                }, 
                "memory": {
                    "required": True, 
                    "type": "object", 
                    "id": "memory", 
                    "properties": {
                        "field": {
                            "required": True, 
                            "type": "string", 
                            "id": "field"
                        }, 
                        "required": {
                            "required": True, 
                            "type": "boolean", 
                            "id": "required"
                        }, 
                        "name": {
                            "required": True, 
                            "type": "string", 
                            "id": "name"
                        }, 
                        "max": {
                            "required": True, 
                            "type": "number", 
                            "id": "max"
                        }
                    }
                }
            }
        }
    }
}

# validate({"name" : "Eggs", "price" : 34.99,'list':[1,5],'address':'bj-jiuxianqiao'}, schema)
validate(structure, schema)


# validate([2, 3, 4], {"maxItems" : 2})                                

