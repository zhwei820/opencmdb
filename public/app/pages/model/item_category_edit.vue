<template>
  <div>
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :span="16">
        <h2><span v-if="id">编辑</span><span v-else>新建</span>CI模型</h2>
        <el-form :model="CICategory" label-position="left">
          <el-form-item label="CI模型名称" :label-width="formLabelWidth">
            <el-input v-model="CICategory.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="CI模型分组" :label-width="formLabelWidth">
            <el-select v-model="CICategory.group" placeholder="请选择">
              <el-option v-bind:label="index" v-bind:value="item" v-for="(item, index) in group_list">
              </el-option>
            </el-select>
          </el-form-item>
          <div class="ci_prop_group" v-for="(ci_prop_group, index_cpg) in CICategory.structure">
            <div class="index_cpg" v-if="index_cpg != 'hidden' && ci_prop_group.length > 0">
              <el-button @click="fold_cpg(index_cpg)" type="nomal" size="mini"> <i :class="{'fa':true, 'fa-plus':CICategory.structure['hidden'][index_cpg], 'fa-minus': !CICategory.structure['hidden'][index_cpg]}"></i>                </el-button>
              {{index_cpg}} 组
              <div v-if="! CICategory.structure['hidden'][index_cpg]">
                <el-form-item v-bind:label="item.name" :label-width="formLabelWidth" v-for="(item, index) in ci_prop_group">
                  <el-tooltip class="item" effect="dark" content="删除!" placement="top-start">
                    <el-button @click="delStructure(index_cpg, index)" type="danger" icon="minus" size="mini" class="del_btn"></el-button>
                  </el-tooltip>
                  <div v-for="(v, i) in item" v-if="">
                    <div v-if="i!='name' && i!='key' && i != 'field'">
                      <div class="prop_label">{{ fields_comment[i] }}</div>
                      <el-switch v-if="i=='required'" on-text="" off-text="" v-model="CICategory.structure[index_cpg][index][i]"></el-switch>
                      <el-input v-else-if="i=='min' || i=='max' " type="number" v-model="CICategory.structure[index_cpg][index][i]" auto-complete="off"></el-input>
                      <el-select v-else-if="i=='reference'" v-model="CICategory.structure[index_cpg][index][i]" placeholder="请选择模型引用">
                        <el-option v-bind:label="item" v-bind:value="index" v-for="(item, index) in item_category_name_list">
                        </el-option>
                      </el-select>
                      <el-input v-else v-model="CICategory.structure[index_cpg][index][i]" auto-complete="off"></el-input>
                    </div>
                    <div v-if="i == 'field'">
                      <div class="prop_label">类型</div>
                      <el-input v-model="fields_comment[v]" auto-complete="off" disabled></el-input>
                    </div>
                    <div v-if="i=='name'||i=='key'">
                      <el-input v-if="i!='required' " v-model="CICategory.structure[index_cpg][index][i]" auto-complete="off" hidden></el-input>
                    </div>
                  </div>
                </el-form-item>
              </div>
            </div>
          </div>
          <el-form-item label="添加属性" :label-width="formLabelWidth">
            <div class="inline">
              <div>名称</div>
              <el-input v-model="tmp_name" auto-complete="off"></el-input>
            </div>
            <div class="inline">
              <div>关键字</div>
              <el-input v-model="tmp_key" auto-complete="off"></el-input>
            </div>
            <div class="inline">
              <div>属性分组(可动态添加)</div>
              <el-select v-model="tmp_group" allow-create filterable="" placeholder="请选择属性分组">
                <!--<el-option label="default" value="default"></el-option>-->
                <el-option v-bind:label="index" v-bind:value="index" v-for="(item, index) in cpg_list">
                </el-option>
              </el-select>
            </div>
            <div>
              <div>类型</div>
              <el-select v-model="field" placeholder="请选择">
                <el-option v-bind:label="fields_comment[index]" v-bind:value="index" v-for="(item, index) in field_list">
                </el-option>
              </el-select>
              <el-button @click="addStructure"><i class="fa fa-plus"></i></el-button>
            </div>
          </el-form-item>
        </el-form>
        <div class="dialog-footer">
          <el-row type="flex" class="row-bg" justify="end">
            <el-col :span="24">
              <el-button size="mini" type="danger" @click="deleteItemCategory()" :class="{'disabled': !this.CICategory.id}">删除</el-button>
            </el-col>
            <el-button type="primary" @click="submit">保存</el-button>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import {
    excel,
    json2url,
    Vue,
    deepCopyOfObject,
    paramParse
  } from "../../assets/js/util.js"

  export default {
    data() {
      return {
        pickerOptions0: {
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7;
          }
        },

        param: {
          start_time: (new Date((new Date()).setDate(new Date().getDate() - 1))),
          end_time: (new Date()),
          name: "",
          value: '',
        },
        input2: "",

        id: 0,
        dialogFormVisible: false,
        formLabelWidth: '120px',
        CICategory: {
          "name": "",
          "id": "",
          group: "default",
          structure: {
            // default: [],
            hidden: {
              // default: false
            }
          },
        },
        _CICategory: {},
        tmp_key: "",
        tmp_name: "",
        tmp_group: "default",
        field_list: {},
        fields_comment: {},
        field: "text",
        cpg_list: {
          default: ""
        },
        group_list: {},
        group_name_list: {},
        item_category_list: {},
        item_category_name_list: {},
      }
    },
    props:['ItemCategoryId'],
    watch: {
      ItemCategoryId: function (dest, src) {
        this.fetch(0, 100)
      }
    },
    beforeMount: function () {
      this._CICategory = deepCopyOfObject(this.CICategory)

      this.get_group_list()
      this.get_field_list()
      this.get_item_category_list()
    },
    methods: {
      get_item_category_list() {
        var query = ""
        this.$http.get("/api/items_categories/" + query).then((response) => {
          if (response.status !== 200) {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          }
          this.item_category_list = {}
          for (var key in response.data) {
            this.item_category_list[response.data[key].name] = response.data[key].id;
          }
          this.item_category_name_list = {}
          for (var key in response.data) {
            this.item_category_name_list[response.data[key].id] = response.data[key].name;
          }

        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        }).then();
      },
      get_group_list() {
        var query = ""
        this.$http.get("/api/groups/" + query).then((response) => {
          this.group_list = {}
          for (var key in response.data) {
            this.group_list[response.data[key].name] = response.data[key].id;
          }
          this.group_name_list = {}
          for (var key in response.data) {
            this.group_name_list[response.data[key].id] = response.data[key].name;
          }

          this.fetch(0, this.pageSize);
        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        }).then();
      },
      get_field_list() {
        var query = ""
        this.$http.get("/api/field_list" + query).then((response) => {
          if (response.status !== 200) {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          }

          this.field_list = response.data['field_list']
          this.fields_comment = response.data['fields_comment']
        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        });
      },
      fetch(offset, limit) {
        // console.log(this.param);
        // var query = json2url(this.param)

        // var id = paramParse('id')
        // var id = this.$route.params.id
        // this.id = id == undefined ? 0 : id

        if (this.ItemCategoryId) {
          this.$http.get("/api/items_categories/" + this.ItemCategoryId + "/?" + Date.now()).then((response) => {
            this.CICategory = response.data
            // debugger
            for (var key in this.CICategory.structure) {
              var rs = this.CICategory.structure[key][0]
              if (key != 'hidden' && rs) {
                Vue.set(this.cpg_list, key, '')
              }
            }

          }, (response) => {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          });
        } else {
          this.CICategory = deepCopyOfObject(this._CICategory)
          this.CICategory.group = this.group_list.default
        }
      },
      addStructure() {
        var tmp = {}
        for (var k in this.field_list[this.field].properties) {
          tmp[k] = "";
        }
        tmp['field'] = this.field;
        tmp['name'] = this.tmp_name;
        tmp['key'] = this.tmp_key;

        this.tmp_name = ""
        this.tmp_key = ""

        if (this.CICategory.structure[this.tmp_group] == undefined) {
          this.CICategory.structure[this.tmp_group] = []
        }
        if (tmp.min != undefined) {
          tmp.min = 1
        }
        if (tmp.min != undefined) {
          tmp.max = 200
        }
        this.CICategory.structure[this.tmp_group].push(tmp)
        Vue.set(this.CICategory.structure['hidden'], this.tmp_group, false)
        Vue.set(this.cpg_list, this.tmp_group, '')
        this.tmp_group = "default"
      },
      delStructure(g, i) {
        this.CICategory.structure[g].splice(i, 1)
      },
      submit() {
        if (!this.CICategory.id) {
          this.$http.post("/api/items_categories/", this.CICategory).then((response) => {
            window.vm_m.get_model_menus()
            // this.$router.push({
            //   path: "/item_category_edit/" + response.data.id
            // })
          }, (response) => {
            parent.vm.show_error_message(response.data.error)
          });

        } else {
          this.$http.put("/api/items_categories/" + this.CICategory.id + "/", this.CICategory).then((response) => {
            window.vm_m.get_model_menus()
            // this.$router.push({
            //   path: "/item_category_edit/" + response.data.id
            // })
          }, (response) => {
            parent.vm.show_error_message(response.data.error)
          });
        }
      },
      fold_cpg(e) {
        if (this.CICategory.structure['hidden'][e]) {
          Vue.set(this.CICategory.structure['hidden'], e, false)
        } else {
          Vue.set(this.CICategory.structure['hidden'], e, true)
        }
      },
      deleteItemCategory() {
        if (this.CICategory.id) {
          this.$http.delete("/api/items_categories/" + this.CICategory.id + "/").then((response) => {
            window.vm_m.get_model_menus()
            window.vm_m.id = ""

          }, (response) => {
            parent.vm.show_error_message(response.data.error)
          });
        }
      }
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
  
  .el-date-editor+.el-select {
    width: 120px;
  }
  
  .el-input {
    width: 150px;
  }
  
  .inline {
    display: inline-block;
  }
  
  .index_cpg {
    font-weight: 700;
  }
  
  .prop_label {
    display: inline-block;
    width: 20%;
  }
</style>