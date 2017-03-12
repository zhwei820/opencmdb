<template>
  <div class="height_100">
    <!--<el-menu theme="dark" default-active="1" class="el-menu-demo" mode="horizontal">
      <el-menu-item index="1">CMDB管理中心</el-menu-item>
    </el-menu>-->
    <el-row class="tac height_100">
      <el-col :span="6">
        <el-menu class="el-menu-vertical-demo" @select="handleSelect" @open="handleOpen">
          <div>
            <el-button size="large" type="primary" class="new_btn" @click="createNewGroup()">
              <i class="fa fa-plus"></i> 新增管理对象
            </el-button>
          </div>
          <el-tree :data="menus" :props="defaultProps" @node-click="handleNodeClick" highlight-current default-expand-all accordion></el-tree>
        </el-menu>
      </el-col>
      <!--sidebar end-->
      <el-col :span=18 class="height_100">
        <el-breadcrumb separator="/" class="breadcrumb_padding">
        </el-breadcrumb>
        <storagegroupedit v-if="path == '/storage_group_edit'" :storage-group-list='name_list' :nested-list="menus" :group-id='id'>
        </storagegroupedit>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import {
    addEvent
  } from "../../assets/js/util.js"
  import StorageGroupEdit from "./storage_group_edit.vue"
  export default {
    data() {
      return {
        breadcrumb1: "dashboard",
        breadcrumb2: "",
        menus: [],
        menus1: {},
        id: "",
        path: "/storage_group_edit",
        _groups: {},
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        group_list: {},
        name_list: {},
      }
    },
    components: {
      storagegroupedit: StorageGroupEdit,
    },
    mounted: function () {
      this.get_model_menus()
      window.vm_m = this
    },
    methods: {
      get_model_menus() {
        var that = this

        // var group_list, group_name_list, group_by_list_of_group
        var p2 = new Promise(
          function (resolve, reject) {
            that.get_model_data("/api/storage_groups/", resolve, reject)
          }
        );

        p2.then((res) => {})
      },

      arrange_group_data(data) {
        var _data_by_id = {}
        this._groups = {}
        for (var index = 0; index < data.length; index++) {
          var element = data[index];
          element.label = element.name
          _data_by_id[element.id] = element
        }

        for (var key in _data_by_id) {
          var element = _data_by_id[key];
          if (this._groups[element.group] == undefined) {
            this._groups[element.group] = {}
            this._groups[element.group].info = _data_by_id[element.id]
            this._groups[element.group].label = _data_by_id[element.id].name
            this._groups[element.group].children = [element]
          } else {
            this._groups[element.group].children.push(element)
          }
        }
        var _g = {}
        if (this._groups[null]) {
          this.recursive_menu_data(this._groups[null])
          this.menus = this._groups[null].children
        }
      },
      recursive_menu_data(g) {
        var d = g.children
        if (d) {
          for (var key1 in d) {
            if (!d[key1].id) {
              continue
            }
            var id = d[key1].id
            if (this._groups[d[key1].id]) {
              var kk = d[key1].id
              d[key1].children = this._groups[kk].children
              this.recursive_menu_data(d[key1])
            }
          }
        }
      },
      get_model_data(url, group_by, resolve, reject) {
        var query = ""
        var list, name_list, group_by_list
        this.$http.get(url + query).then((response) => {

          list = {}
          for (var key in response.data) {
            list[response.data[key].name] = response.data[key].id;
          }
          name_list = {}
          for (var key in response.data) {
            name_list[response.data[key].id] = response.data[key].name;
          }

          this.arrange_group_data(response.data)
          this.name_list = name_list
          this.group_list = list
          resolve([list])
        }, (response) => {
          console.log(response.data.detail);
          var msg = response.data.detail != undefined ? response.data.detail : response.data.error
          parent.vm.show_error_message(msg)
        });
      },
      handleSelect(key, keyPath) {
        this.id = key
        this.path = "/storage_group_edit"
      },
      handleOpen(key, keyPath) {
        if (key != "/") {}
      },
      createNewGroup() {
        this.id = ""
        this.path = "/storage_group_edit"
      },
      editGroup(id, e) {
        this.id = id
        this.path = "/storage_group_edit"
        e.stopPropagation()
      },
      show_error_message(msg) {
        this.$message({
          type: 'info',
          message: msg
        });
      },
      handleNodeClick(data) {
        // console.log(this.group_list[data.label]);
        this.id = this.group_list[data.label]
      }
    },
  }
</script>
<style scoped>
  @import '../../assets/css/normalize.css';
  @import '../../assets/css/index.css';
  body {
    font-family: Helvetica, sans-serif;
  }
  
  .new_btn {
    margin-left: -70px;
    left: 50%;
    position: relative;
    margin-bottom: 3px;
    width: 153px;
  }
  
  .edit_mini_btn {
    background: transparent;
    border: navajowhite;
  }
</style>