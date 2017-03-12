## 创建层

**接口地址：**

> BASE_URL/api/layers/

**请求方法：**

POST

**请求参数：**

    {
        "name": "create_layer1"
    }

**参数说明：**

> name: string, 层名字，需要保证唯一性

**返回结果示例：**

成功：

    http status 201
    
    {
        "id": "5833a9251774d5078c6bd18f",
        "name": "create_layer1"
    }

## 修改层

**接口地址：**

> BASE_URL/api/layers/(id)/

**请求方法：**

PUT

**请求参数：**

    {
        "name": "create_layer1"
    }

**参数说明：**

> name: string, 层名字，需要保证唯一性

**返回结果示例：**

成功：

    http status 200
    
    {
        "id": "5833a9251774d5078c6bd18f",
        "name": "create_layer1"
    }

## 查看具体层

**接口地址：**

> BASE_URL/api/layers/(id)/

**请求方法：**

GET

**返回结果示例：**

成功：

    http status 200
    
    {
        "id": "5833a9251774d5078c6bd18f",
        "name": "create_layer5"
    }

## 查看所有层

**接口地址：**

> BASE_URL/api/layers/

**请求方法：**

GET

**返回结果示例：**

成功：

    http status 200
    
    [
        {
            "id": "583285cb1774d50ea85802f8",
            "name": "create_layer1"
        },
        {
            "id": "5833a9251774d5078c6bd18f",
            "name": "create_layer3"
        }
    ]
    
## 删除层
    
**接口地址：**

> BASE_URL/api/layers/(id)/

**请求方法：**

DELETE

**返回结果示例：**

成功：

    http status 204

## 创建组

**接口地址：**

> BASE_URL/api/groups/

**请求方法：**

POST

**请求参数：**

    {
        "name": "create_group1",
        "layer": "583285cb1774d50ea85802f8"
    }

**参数说明：**

> name: string, 组名字，需要和layer保证联合唯一性
> layer: string(24位), 所属层ID

**返回结果示例：**

成功：

    http status 201
    
    {
        "id": "5833a9251774d5078c6bd18f",
        "name": "create_layer1",
        "layer": "583285cb1774d50ea85802f8"
    }

## 修改组

**接口地址：**

> BASE_URL/api/groups/(id)/

**请求方法：**

PUT

**请求参数：**

    {
        "name": "create_layer1",
        "layer": "583285cb1774d50ea85802f8"
    }

**参数说明：**

> name: string, 组名字，需要和layer保证联合唯一性
> layer: string(24位), 所属层ID

**返回结果示例：**

成功：

    http status 200
    
    {
        "id": "5833a9251774d5078c6bd18f",
        "name": "create_layer1",
        "layer": "583285cb1774d50ea85802f8"
    }

## 查看具体组

**接口地址：**

> BASE_URL/api/groups/

**请求方法：**

GET

**返回结果示例：**

成功：

    http status 200
    
    {
        "id": "5833a9251774d5078c6bd18f",
        "name": "create_layer1",
        "layer": "583285cb1774d50ea85802f8"
    }

## 查看某一层的所有组

**接口地址：**

> BASE_URL/layers/(id)/groups/

**请求方法：**

GET

**参数说明：**

>id: 层ID

**返回结果示例：**

成功：

    http status 200
    
    [
        {
            "id": "583285cb1774d50ea85802f8",
            "name": "create_group1"
        },
        {
            "id": "5833a9251774d5078c6bd18f",
            "name": "create_group3"
        }
    ]
    
## 删除组
    
**接口地址：**

> BASE_URL/api/groups/(id)/

**请求方法：**

DELETE

**返回结果示例：**

成功：

    http status 204

## 创建CI模型

**接口地址：**

> BASE_URL/api/categories/

**请求方法：**

POST

**请求参数：**

    {
        "name": "create_ci2",
        "group": "583286441774d5112845e0f6",
        "structure": {
            "system": {
                "disk": {
                    "field": "string",
                    "required": "True",
                    "default": "233",
                    "valid_rule": "none",
                    "max_length": "20",
                    "min_length": "1"
                }
            },
            "default": {
                "price": {
                    "field": "string",
                    "required": "True",
                    "default": "233",
                    "valid_rule": "none",
                    "max_length": "20",
                    "min_length": "1"
                }
            }
        }
    }

**参数说明：**

> name: string, CI模型名字，需要和group保证联合唯一性
> group: string(24位), 所属组ID
> structure: dict, 模型的属性组和具体属性设置

**返回结果示例：**

成功：

    http status 201
    
    {
        "id": "583292ca1774d51edc1f970b",
        "name": "create_ci2",
        "structure": {
            "system": {
                "disk": {
                    "max_length": "20",
                    "default": "233",
                    "min_length": "1",
                    "required": "True",
                    "field": "string",
                    "valid_rule": "none"
                }
            },
            "default": {
                "price": {
                    "max_length": "20",
                    "default": "233",
                    "min_length": "1",
                    "required": "True",
                    "field": "string",
                    "valid_rule": "none"
                }
            }
        },
        "group": "583286441774d5112845e0f6"
    }

## 修改CI模型

**接口地址：**

> BASE_URL/api/categories/(id)/

**请求方法：**

PUT

**请求参数：**

    {
        "name": "create_ci2",
        "group": "5833d9ae1774d5078c6bd190",
        "structure": {
          "default": {
            "price": {
              "max_length": "20",
              "default": "233",
              "min_length": "1",
              "field": "string",
              "required": "True",
              "valid_rule": "none"
            }
          },
          "system": {
            "disk": {
              "max_length": "20",
              "default": "233",
              "min_length": "1",
              "field": "string",
              "required": "True",
              "valid_rule": "none"
            }
          }
        }
    }

**参数说明：**

> name: string, CI模型名字，需要和group保证联合唯一性
> group: string(24位), 所属组ID
> structure: dict, 模型的属性组和具体属性设置

**返回结果示例：**

成功：

    http status 200
    
    {
        "id": "5832c0461774d526b092103c",
        "name": "create_ci2",
        "group": "5833d9ae1774d5078c6bd190",
        "structure": {
          "default": {
            "price": {
              "max_length": "20",
              "default": "233",
              "min_length": "1",
              "field": "string",
              "required": "True",
              "valid_rule": "none"
            }
          },
          "system": {
            "disk": {
              "max_length": "20",
              "default": "233",
              "min_length": "1",
              "field": "string",
              "required": "True",
              "valid_rule": "none"
            }
          }
        }
    }

## 查看具体CI模型

**接口地址：**

> BASE_URL/api/categories/(id)/

**请求方法：**

GET

**返回结果示例：**

成功：

    http status 200
    
    {
        "id": "5832c0461774d526b092103c",
        "name": "create_ci2",
        "structure":{
        "system":{
            "disk":{
                    "max_length": "20",
                    "default": "233",
                    "field": "string",
                    "min_length": "1",
                    "valid_rule": "none",
                    "required": "True"
                }
            },
            "default":{
                "price":{
                    "max_length": "20",
                    "default": "233",
                    "field": "string",
                    "min_length": "1",
                    "valid_rule": "none",
                    "required": "True"
                }
            }
        },
        "group": "5833d9ae1774d5078c6bd190"
    }

## 查看某一组的所有CI模型

**接口地址：**

> BASE_URL/api/groups/(id)/categories/

**请求方法：**

GET

**参数说明：**

>id: 组ID

**返回结果示例：**

成功：

    http status 200
    
    [
        {
            "id": "5832ab5a1774d53110436435",
            "name": "我是测试",
            "structure": {
                "system": {
                    "disk": {
                        "max_length": "20",
                        "default": "233",
                        "field": "string",
                        "min_length": "1",
                        "valid_rule": "none",
                        "required": "True"
                    }
                },
                "default": {
                    "price": {
                        "max_length": "20",
                        "default": "233",
                        "field": "string",
                        "min_length": "1",
                        "valid_rule": "none",
                        "required": "True"
                    }
                }
            },
            "group": "583286441774d5112845e0f6"
        }
    ]

## 查看所有CI模型

**接口地址：**

> BASE_URL/api/categories/

**请求方法：**

GET

**返回结果示例：**

成功：

    http status 200
    
    [
        {
            "id": "5832ab5a1774d53110436435",
            "name": "我是测试",
            "structure": {
                "system": {
                    "disk": {
                        "max_length": "20",
                        "default": "233",
                        "field": "string",
                        "min_length": "1",
                        "valid_rule": "none",
                        "required": "True"
                    }
                },
                "default": {
                    "price": {
                        "max_length": "20",
                        "default": "233",
                        "field": "string",
                        "min_length": "1",
                        "valid_rule": "none",
                        "required": "True"
                    }
                }
            },
            "group": "583286441774d5112845e0f6"
        },
        {
            "id": "5832c0461774d526b092103c",
            "name": "create_ci2",
            "structure": {
                "system": {
                    "disk": {
                        "max_length": "20",
                        "default": "233",
                        "field": "string",
                        "min_length": "1",
                        "valid_rule": "none",
                        "required": "True"
                    }
                },
                "default": {
                    "price": {
                        "max_length": "20",
                        "default": "233",
                        "field": "string",
                        "min_length": "1",
                        "valid_rule": "none",
                        "required": "True"
                    }
                }
            },
            "group": "5833d9ae1774d5078c6bd190"
        }
    ]
    
## 删除CI模型
    
**接口地址：**

> BASE_URL/api/categories/(id)/

**请求方法：**

DELETE

**返回结果示例：**

成功：

    http status 204

## 创建CI对象

**接口地址：**

> BASE_URL/api/items/

**请求方法：**

POST

**请求参数：**

    {
        "name": "create_ci2",
        "category": "5832c0461774d526b092103c",
        "structure": {
            "system": {
                "disk": "224"
            },
            "default": {
                "price": "225"
            }
        }
    }

**参数说明：**

> name: string, 对象名字，需要和category保证联合唯一性
> category: string(24位), 所属层ID
> structure: dict, 对象的属性组和具体属性值

**返回结果示例：**

成功：

    http status 201
    
    {
        "id": "5833e1511774d5078c6bd191",
        "name": "create_ci2",
        "category": "5832c0461774d526b092103c",
        "structure": {
            "system": {
                "disk": "224"
            },
            "default": {
                "price": "225"
            }
        }
    }

## 修改CI对象

**接口地址：**

> BASE_URL/api/items/(id)/

**请求方法：**

PUT

**请求参数：**

    {
        "name": "create_ci2",
        "category": "5832c0461774d526b092103c",
        "structure": {
            "system": {
                "disk": "224"
            },
            "default": {
                "price": "225"
            }
        }
    }

**参数说明：**

> name: string, 对象名字，需要和category保证联合唯一性
> category: string(24位), 所属层ID
> structure: dict, 对象的属性组和具体属性值

**返回结果示例：**

成功：

    http status 200
    
    {
        "id": "5833e1511774d5078c6bd191",
        "name": "create_ci2",
        "category": "5832c0461774d526b092103c",
        "structure": {
            "system": {
                "disk": "224"
            },
            "default": {
                "price": "225"
            }
        }
    }

## 查看具体CI对象

**接口地址：**

> BASE_URL/api/items/(id)/

**请求方法：**

GET

**返回结果示例：**

成功：

    http status 200
    
    {
        "id": "5833e1511774d5078c6bd191",
        "name": "create_ci2",
        "category": "5832c0461774d526b092103c",
        "structure": {
            "system": {
                "disk": "224"
            },
            "default": {
                "price": "225"
            }
        }
    }

## 查看某一CI模型的所有CI对象

**接口地址：**

> BASE_URL/api/categories/(id)/items/

**请求方法：**

GET

**参数说明：**

>id: CI模型ID

**返回结果示例：**

成功：

    http status 200
    
    [
        {
            "id": "5833e1511774d5078c6bd191",
            "name": "create_ci2",
            "category": "5832c0461774d526b092103c",
            "structure": {
                "system": {
                    "disk": "224"
                },
                "default": {
                    "price": "225"
                }
            }
        }
    ]
    
## 删除CI对象
    
**接口地址：**

> BASE_URL/api/items/(id)/

**请求方法：**

DELETE

**返回结果示例：**

成功：

    http status 204
