<template>
  <div v-if="categoryId">
    <el-button type="primary" size="large" @click="createNewCIItem()">新建</el-button>
    <el-button type="primary" class="r fa fa-share-square-o" @click="saveExcel"></el-button>
    <el-input placeholder="搜索" class="right_search" icon="search" v-model="input2" @click="handleIconClick" @keyup.enter.native="handleIconClick">
    </el-input>
    <el-button type="default" class="r fa fa-refresh" @click="refresh_data"></el-button>
    <el-table :data="tableData" border style="width: 100%" height="920">
      <el-table-column fixed :context="_self" inline-template label="操作" width="150">
        <div>
          <el-button size="small" @click="handleEdit($index, row)">
            编辑
          </el-button>
          <el-button size="mini" type="danger" @click="handleDelete($index, row)">
            删除
          </el-button>
        </div>
      </el-table-column>
      <el-table-column prop="name" :label=tableHead.name width="120">
      </el-table-column>
      <el-table-column :prop="item.key" :label=item._name width="120" v-for="(item, index) in item_category._structure" v-if="item.field != 'image'">
      </el-table-column>
      <el-table-column :prop="item.key" :label=item._name width="240" v-for="(item, index) in item_category._structure" v-if="item.field == 'image'">
        <template scope="scope">
          <img :src="scope.row[item.key]" height="60" @click="show_image(scope.row[item.key])" />
        </template>
      </el-table-column>
      <!--<el-table-column prop="group_name" :label=tableHead.group_name width="120">
      </el-table-column>-->
    </el-table>
    <div class="block">
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="tablePage" :page-sizes="[20, 50, 100, 200, 400]"
        :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="totalNum">
        </el-pagination>
    </div>

<el-dialog title="提示" v-model="dialogVisible" size="tiny">
  <img :src="tmp_image_src" height="100%" width="100%"/>  
  <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="dialogVisible = false">关 闭</el-button>
  </span>
</el-dialog>


    <el-dialog title="" v-model="dialogFormVisible" class="item_edit_dialog">
      <h2><span v-if="CIItem.id">编辑</span><span v-else>新建</span> {{CIItem._category.name}} </h2>
      <el-form :model="CIItem" label-position="left">
        <el-form-item label="名称" :label-width="formLabelWidth">
          <el-input v-model="CIItem.name" auto-complete="off"></el-input>
        </el-form-item>
        <div v-for="(v, index_cpg) in CIItem._category.structure" v-if="index_cpg != 'hidden' && v.length > 0">
          <el-button @click="fold_cpg(index_cpg)" type="nomal" size="mini">
            <i :class="{'fa':true, 'fa-plus':CIItem._category.structure['hidden'][index_cpg], 'fa-minus': !CIItem._category.structure['hidden'][index_cpg]}"></i>
          </el-button>
          {{index_cpg}} 组
          <div v-if="! CIItem._category.structure['hidden'][index_cpg]">
            <el-form-item :label="v1.name" :label-width="formLabelWidth" v-for="v1 in v">
              <div v-if="v1.field == 'string' || v1.field == 'number'">
                <el-input :type="v1.field == 'number'?'number':'text'" v-model="CIItem[v1.key]" auto-complete="off"></el-input><span v-if="v1.field == 'number'"> {{v1.unit}}</span>
              </div>
              <div v-if="v1.field == 'text'">
                <el-input type="textarea" :autosize="{ minRows: 3, maxRows: 5}" v-model="CIItem[v1.key]" auto-complete="off" width="300"></el-input>
              </div>
              <div v-if="v1.field == 'ref'">
                <el-select v-model="CIItem[v1.key]">
                  <el-option v-for="item in tmp_ref_ci_list[v1.key]" v-bind:label="item.name" v-bind:value="item.id">
                    {{ item.name }}
                  </el-option>
                </el-select> {{tmp_item_category.name}} 引用
              </div>
              <div v-if="v1.field == 'multi_select' || v1.field == 'select'">
                <el-select v-model="CIItem[v1.key]" :multiple="v1.field == 'multi_select'">
                  <el-option v-for="item in v1._choice" v-bind:value="item">
                    {{ item }}
                  </el-option>
                </el-select>
              </div>
              <div v-if="v1.field == 'datetime'">
                <el-date-picker v-model="CIItem[v1.key]" type="datetime" placeholder="选择日期时间">
                </el-date-picker>
              </div>
              <div v-if="v1.field == 'image'">
                <el-upload action="/api/upload_file/" type="drag" :thumbnail-mode="true" :before-upload="beforeUpload(v1.key)" :on-success="handleSuccess"
                  :on-preview="handlePreview" :on-remove="handleRemove" :default-file-list="fileList[v1.key]">
                  <i class="el-icon-upload"></i>
                  <div class="el-dragger__text">将文件拖到此处，或<em>点击上传</em></div>
                  <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
                  </el-upload>
                  <!--{{CIItem[v1.key]}}-->
                  <!--<select multiple hidden name="" v-model="CIItem[v1.key]" id="" />-->
              </div>
              类型：{{fields_comment[v1.field]}}, <span v-if="v1.field == 'string' || v1.field == 'number'">最大/最长： {{v1.max}}, 最小: {{v.min}}, </span>
            </el-form-item>
          </div>
        </div>
        <div class="ci_prop_group" v-for="(ci_prop_group, index_cpg) in CIItem.structure">
        </div>
      </el-form>
      <div class="dialog-footer">
        <el-row type="flex" class="row-bg" justify="end">
          <el-button type="primary" @click="submit">确 定</el-button>
        </el-row>
      </div>
    </el-dialog>
  </div>
</template>
<script>
  import {
    excel,
    json2url,
    Vue,
    deepCopyOfObject
  } from "../../assets/js/util.js"

  export default {
    data() {
      return {
        pickerOptions0: {
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7;
          }
        },
        dialogTableVisible: false,
        id: false,
        param: {
          start_time: (new Date((new Date()).setDate(new Date().getDate() - 1))),
          end_time: (new Date()),
          name: "",
          value: '',
        },
        input2: "",
        tableHead: {
          "name": "CI模型实例名称",
          group_name: "CI模型分组名称",
        },
        tableHeadKeys: [
          "date",
          "name",
          "group_name",
        ],
        tableData1: [],
        tableData: [],
        tablePage: 1,
        pageSize: 20,
        totalNum: 1,

        dialogFormVisible: false,
        formLabelWidth: '120px',

        CIItem: {
          "name": "",
          "id": "",
          _category: {
            name: ""
          },
        },
        // tmp_key: "",
        // tmp_name: "",
        // tmp_group: "default",
        field: "",
        cpg_list: {
          default: ""
        },
        item_category: {},
        field_list: {},
        fields_comment: {},
        im_k: "",
        fileList: {},
        tmp_ref_ci_list: {},
        tmp_item_category: "",
        dialogVisible:false,
        tmp_image_src:"",
      }
    },
    props: ['categoryId'],
    watch: {
      categoryId: function (to, from) {
        this.fetch(0, this.pageSize)
      }
    },
    beforeMount: function () {
      window.vm_n = this
      this.fetch(0, this.pageSize);
      this.get_field_list()
    },
    methods: {
      get_ref_ci_list(id, key) {
        this.$http.get("/api/items_categories/" + id + '/items').then((response) => {
          this.tmp_ref_ci_list[key] = response.data
          var _tableData1 = deepCopyOfObject(this.tableData1)
          for (var key0 in _tableData1) {
            var element = _tableData1[key0];
            for (var key1 in response.data) {
              var element1 = response.data[key1];
              if (element[key] == element1.id) {
                element['_' + key] = element1.name
              }
            }
          }
          this.tableData1 = _tableData1

          var _tableData = deepCopyOfObject(this.tableData)
          for (var key0 in _tableData) {
            var element = _tableData[key0];
            for (var key1 in response.data) {
              var element1 = response.data[key1];
              if (element[key] == element1.id) {
                element['_' + key] = element1.name

              }
            }
          }
          this.tableData = _tableData

        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        });
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
      get_item_category_by_id(id, key) {
        this.$http.get("/api/items_categories/" + id).then((response) => {
          this.tmp_item_category = response.data

        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        });
      },
      get_item_category() {
        this.$http.get("/api/items_categories/" + this.categoryId).then((response) => {
          this.item_category = response.data
          this.item_category._structure = []

          for (var key in this.item_category.structure) {
            var element = this.item_category.structure[key];
            var element1 = deepCopyOfObject(element)
            if (!key || key == "hidden") {
              continue
            }
            for (var key1 in element) {
              if (element[key1].field != undefined && (element[key1].field == "select" || element[key1].field ==
                  "multi_select")) {
                this.item_category.structure[key][key1]._choice = this.item_category.structure[key][key1].choice.split(
                  "|")
              }
              if (element[key1].field == "ref") {
                console.log(this.item_category.structure[key][key1].reference);
                this.get_ref_ci_list(this.item_category.structure[key][key1].reference, element[key1].key)
                this.get_item_category_by_id(this.item_category.structure[key][key1].reference, element[key1].key)
                element1[key1].key = "_" + element[key1].key
              }
              if (element[key1].field == "image") {
                element1[key1].key = "_" + element[key1].key
              }
              if (element1[key1].field == "number") {
                element1[key1]._name = element1[key1].name + " (" + element1[key1].unit + ")"
              } else {
                element1[key1]._name = element1[key1].name
              }
            }
            this.item_category._structure = this.item_category._structure.concat(element1)
          }
          // console.log(this.item_category._structure);

        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        });
      },
      fetch() {
        if (this.categoryId) {
          this.$http.get("/api/items_categories/" + this.categoryId + '/items').then((response) => {
            var res = response.data
            for (var key1 in res) {
              var element1 = res[key1];
              for (var key2 in element1) {
                var element2 = element1[key2];
                if (typeof (element2) == "object" && element2[0].url) {
                  res[key1]["_" + key2] = element2[0].url
                }
              }
            }

            this.tableData1 = res
            this.tableData = this.tableData1.slice(0, this.pageSize)
            this.totalNum = this.tableData1.length
            this.handleIconClick()
            this.get_item_category()

          }, (response) => {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          });
        }
      },
      handleEdit(index, row) {
        var _CIItem = deepCopyOfObject(row)

        _CIItem._category = this.item_category,
          this.dialogFormVisible = true
        for (var key in this.item_category.structure) {
          var element = this.item_category.structure[key];
          for (var key1 in element) {
            if (_CIItem[element[key1].key] == undefined) {
              _CIItem[element[key1].key] = ""
            }

            if ((element[key1].field == "multi_select") && typeof (_CIItem[element[key1].key]) == "string") {
              _CIItem[element[key1].key] = [_CIItem[element[key1].key]]
            }
            if (element[key1].field == "image") {
              if (typeof (_CIItem[element[key1].key]) == "string") {
                _CIItem[element[key1].key] = []
              }
              var fl = deepCopyOfObject(this.fileList)
              fl[element[key1].key] = _CIItem[element[key1].key]
              this.fileList = fl
            }
          }
        }

        this.CIItem = _CIItem
        console.log(this.CIItem);

      },
      createNewCIItem() {
        this.dialogFormVisible = true
        var _CIItem = {
          "name": "",
          "id": "",
          _category: this.item_category,
          category: this.categoryId,
        }
        for (var key in this.item_category.structure) {
          var element = this.item_category.structure[key];
          for (var key1 in element) {
            if (element[key1].field == "multi_select") {
              element[key1].default = [this.item_category.structure[key][key1]._choice[0]] //multi_select 默认是array
            }
            if (element[key1].field == "image") {
              element[key1].default = [] //image 默认是array
              var k = element[key1].key
              this.fileList = {
                k: []
              }
            }
            if (element[key1].key != undefined) {
              _CIItem[element[key1].key] = element[key1].default || ''
            }
          }
        }

        this.CIItem = _CIItem
      },
      handleDelete(index, row) {
        this.$confirm('此操作将永久删除' + row.name + ', 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$http.delete("/api/items/" + row.id + "/").then((response) => {
            this.dialogFormVisible = false
            this.fetch()
          }, (response) => {
            parent.vm.show_error_message(response.data.error)
          });
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      submit() {
        var ci_item = deepCopyOfObject(this.CIItem)
        ci_item.group = ci_item._category.group
        delete ci_item._category
        if (!this.CIItem.id) {
          delete ci_item.id
          this.$http.post("/api/items/", ci_item).then((response) => {
            this.dialogFormVisible = false
            this.fetch()
          }, (response) => {
            parent.vm.show_error_message(response.data.error)
          });
        } else {
          this.$http.put("/api/items/" + this.CIItem.id + "/", ci_item).then((response) => {
            this.dialogFormVisible = false
            this.fetch()
          }, (response) => {
            parent.vm.show_error_message(response.data.error)
          });
        }
      },
      handleIconClick(ev) {
        if (this.input2) {
          var tmp = []
          for (var ii = 0; ii < this.tableData1.length; ii++) {
            for (var jj in this.tableData1[ii]) {
              if (("" + this.tableData1[ii][jj]).indexOf(this.input2) >= 0) {
                tmp.push(this.tableData1[ii])
                break
              }
            }
          }
          this.tableData = tmp
        } else {
          this.tableData = this.tableData1
        }
        // this.totalNum = this.tableData.length
      },
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
        this.tableData = this.tableData1.slice((val - 1) * this.pageSize, (val) * this.pageSize)
      },
      saveExcel() {
        excel([this.tableHead].concat(this.tableData1), this.tableHeadKeys, "aaa", "xls")
      },
      refresh_data() {
        this.fetch(0, this.pageSize)
      },
      fold_cpg(e) {
        if (this.CIItem._category.structure['hidden'][e]) {
          this.CIItem._category.structure['hidden'][e] = false
        } else {
          this.CIItem._category.structure['hidden'][e] = true
        }
      },
      handleRemove(file, fl) {
        console.log(file, fl);
      },
      handlePreview(file) {
        console.log(file);
      },
      handleSuccess(data) {
        this.CIItem[this.im_k].push(data)
      },
      beforeUpload(k) {
        this.im_k = k
      },
      show_image(src){
        this.dialogVisible = true
        this.tmp_image_src = src
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
  
  .el-date-editor+.el-select {
    width: 120px;
  }
  
  .el-input {
    width: 250px;
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
  
  .multi_select {
    height: 200px
  }
</style>