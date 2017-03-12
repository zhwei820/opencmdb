<template>
  <div>
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :span="6">
        <h2><span v-if="id">编辑</span><span v-else>新建</span>CI模型组</h2>
        <el-form label-position="top">
          <el-form-item label="CI模型组名称">
            <el-input v-model="form.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="CI模型层">
            <el-select v-model="form.layer" placeholder="请选择">
              <el-option v-bind:label="index" v-bind:value="item" v-for="(item, index) in layer_list">
              </el-option>
            </el-select>
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
          layer: "default",
        },
        _form: {},
        layer_list: {},
        layer_name_list: {},
        formLabelWidth: '120px',
        id: 0,
      }
    },
    props: ['groupId'],
    watch: {
      groupId: function (dest, src) {
        this.fetch(0, 100)
      }
    },
    beforeMount: function () {
      window.vm_m_n = this;
      this._form = deepCopyOfObject(this.form)
      this.get_layer_list()
    },
    methods: {
      get_layer_list() {
        var query = ""
        this.$http.get("/api/layers/" + query).then((response) => {
          this.layer_list = {}
          for (var key in response.data) {
            this.layer_list[response.data[key].name] = response.data[key].id;
          }
          this.layer_name_list = {}
          for (var key in response.data) {
            this.layer_name_list[response.data[key].id] = response.data[key].name;
          }
          this.fetch(0, 100)
        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        });
      },
      fetch(offset, limit) {
        // var id = paramParse('id')
        // var id = this.$route.params.id
        // this.id = id == undefined ? 0 : id
        if (this.groupId) {
          this.$http.get("/api/groups/" + this.groupId + "/?" + Date.now()).then((response) => {
            this.form = response.data

          }, (response) => {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          });
        } else {
          this.form = deepCopyOfObject(this._form)
          this.form.layer = this.layer_list.default
        }
      },
      submit() {
        if (!this.form.id) {
          this.$http.post("/api/groups/", this.form).then((response) => {
            window.vm_m.get_model_menus()
            // this.$router.push({
            //   path: "/group_edit/" + response.data.id
            // })

          }, (
            response) => {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          });

        } else {
          this.$http.put("/api/groups/" + this.form.id + "/", this.form).then((response) => {
            window.vm_m.get_model_menus()
            // this.$router.push({
            //   path: "/group_edit/" + response.data.id
            // })
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
          this.$http.delete("/api/groups/" + this.form.id + "/").then((response) => {
            window.vm_m.id = ""

          }, (response) => {
            parent.vm.show_error_message(response.data.error)
          });
        }
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