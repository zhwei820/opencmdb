<template>
  <div>
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :span="15">
        <h2><span v-if="groupId">编辑</span><span v-else>新建</span>管理项目</h2>
        <el-form label-position="left" label-width="80px">
          <el-form-item label="管理项目名称">
            <el-input v-model="form.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="父项目 (可为空)">
            <el-select v-model="form.group" placeholder="请选择">
              <el-option v-bind:label="item" v-bind:value="index" v-for="(item, index) in storageGroupListExceptOwnGroup">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="item.group_name" v-for="(item, index) in form" v-if="index.length == 24">
            <el-input v-model="item.name" auto-complete="off" disabled></el-input>
            <el-tooltip class="item" effect="dark" content="删除!" placement="top-start">
              <el-button @click="delResource(index)" type="danger" icon="minus" size="mini" class="del_btn"></el-button>
            </el-tooltip>
          </el-form-item>
          <el-form-item label="添加资源" :label-width="formLabelWidth">
            <div>
              <el-select v-model="tmp_item" placeholder="请选择">
                <el-option-group v-for="group in items_by_group" :label="group.label">
                  <el-option v-for="item in group.options" :label="item.label" :value="item.id">
                  </el-option>
                </el-option-group>
              </el-select>
              <el-button @click="addResource"><i class="fa fa-plus"></i></el-button>
            </div>
          </el-form-item>
        </el-form>
        <div class="dialog-footer">
          <el-row type="flex" class="row-bg" justify="end">
            <el-col :span="24">
              <el-button size="mini" type="danger" @click="deleteGroup()" :class="{'hidden': !this.form.id || this.form.name == 'default'}">删除</el-button>
            </el-col>
            <el-button type="primary" @click="submit">确 定</el-button>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import {
    excel,
    deepCopyOfObject,
    paramParse
  } from "../../assets/js/util.js"

  export default {
    data() {
      return {
        input2: "",

        dialogFormVisible: false,
        form: {
          name: '',
          id: "",
          group: ""
        },
        _form: {},
        layer_list: {},
        layer_name_list: {},
        formLabelWidth: '120px',
        id: 0,
        storageGroupListExceptOwnGroup: {},
        filter_ids: [],
        tmp_item: "",
        items_by_group: [],
      }
    },
    props: ['groupId', 'storageGroupList', 'nestedList'],
    watch: {
      groupId: function (dest, src) {
        this.fetch(0, 100)
      },
      storageGroupList: function (dest, src) {
        this.fetch(0, 100)
      }
    },
    mounted: function () {
      this._form = deepCopyOfObject(this.form)
      this.fetch(0, 100)
      this.get_item_data()
      window.vm_m_n = this;
    },
    methods: {
      get_item_data() {
        var that = this
        // var group_list, group_name_list, group_by_list_of_group
        var p1 = new Promise(
          function (resolve, reject) {
            that.get_item_groups(resolve, reject)
            return p2
          }
        );
        var p2 = new Promise(
          function (resolve, reject) {
            that.get_items(resolve, reject)
          }
        );
        p1.then((res) => {}).then((res) => {})
      },
      get_item_groups(resolve, reject) {
        this.$http.get("/api/groups/" + "?t=" + Date.now()).then((response) => {
          this.group_name_list = {}
          for (var key in response.data) {
            this.group_name_list[response.data[key].id] = response.data[key].name;
          }
          resolve()
        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        });
      },
      get_items(resolve, reject) {
        this.$http.get("/api/items/" + "?t=" + Date.now()).then((response) => {
          this.CICategory = response.data
          this.items_name_list = {}
          for (var key in response.data) {
            this.items_name_list[response.data[key].id] = response.data[key];
          }
          var _items_by_group = {}
          for (var key in response.data) {
            var element = response.data[key]
            if (_items_by_group[element.group] == undefined) {
              _items_by_group[element.group] = {}
              _items_by_group[element.group].id = element.group
              _items_by_group[element.group].label = this.group_name_list[element.group]
              _items_by_group[element.group].options = []
            }
            element.label = element.name
            _items_by_group[element.group].options.push(element);
          }
          this.items_by_group = []
          for (var key in _items_by_group) {
            this.items_by_group.push(_items_by_group[key])
          }
          // console.log(this.items_by_group);
          resolve()
        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        });
      },
      recursive_filter(children, id) { // 过滤本组id
        for (var key in children) {
          var element = children[key];
          if (element.id == id) {
            this.filter_ids.push(id)
            this.recursive_get_ids(element.children)
          } else {
            this.recursive_filter(element.children, id)
          }
        }
      },
      recursive_get_ids(children) {
        for (var key in children) {
          var element = children[key];
          this.filter_ids.push(element.id)
          this.recursive_get_ids(element.children)
        }
      },
      fetch(offset, limit) {
        // var id = paramParse('id')
        // var id = this.$route.params.id
        // this.id = id == undefined ? 0 : id
        this.filter_ids = []
        // console.log(this.groupId);
        var tmp = deepCopyOfObject(this.storageGroupList)
        this.storageGroupListExceptOwnGroup = tmp
        this.recursive_filter(this.nestedList, this.groupId)
        // console.log(this.filter_ids);
        for (var ii = 0; ii < this.filter_ids.length; ii++) {
          delete this.storageGroupListExceptOwnGroup[this.filter_ids[ii]]
        }
        this.storageGroupListExceptOwnGroup[''] = '空'

        if (this.groupId) {
          this.$http.get("/api/storage_groups/" + this.groupId + "/?t=" + Date.now()).then((response) => {
            this.form = response.data
            if (!this.form.group) {
              this.form.group = ""
            }
            // console.log(this.form);
          }, (response) => {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          });
        } else {
          var form = deepCopyOfObject(this._form)
          form.group = ''
          this.form = form
        }
      },
      submit() {
        if (!this.form.id) {
          delete this.form.id
          this.$http.post("/api/storage_groups/", this.form).then((response) => {
            window.vm_m.get_model_menus()
            this.groupId = response.data.id
          }, (
            response) => {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          });
        } else {
          this.$http.put("/api/storage_groups/" + this.form.id + "/", this.form).then((response) => {
            window.vm_m.get_model_menus()
            this.groupId = response.data.id
          }, (
            response) => {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          });
        }
      },
      deleteGroup() {
        if (this.form.id) {
          this.$http.delete("/api/storage_groups/" + this.form.id + "/").then((response) => {
            window.vm_m.id = ""
            window.vm_m.get_model_menus()
          }, (response) => {
            parent.vm.show_error_message(response.data.error)
          });
        }
      },
      addResource() {
        if (!this.tmp_item) {
          this.$message({
            type: 'info',
            message: '请选择资源！'
          });
          return
        }
        var _form = deepCopyOfObject(this.form)
        _form[this.tmp_item] = this.items_name_list[this.tmp_item]
        _form[this.tmp_item].group_name = this.group_name_list[_form[this.tmp_item].group]
        this.form = _form
      },
      delResource(index) {
        var _form = deepCopyOfObject(this.form)
        delete _form[index]
        this.form = _form
      },
    }
  }
</script>
<style scoped>
  @import '../../assets/css/normalize.css';
  @import '../../assets/css/index.css';
  .right_search {
    float: right;
    width: 20%;
  }
  
  .right_export {
    float: right;
  }
</style>