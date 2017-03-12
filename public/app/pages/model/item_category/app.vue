<template>
  <div>
    <el-date-picker v-model="param.start_time" type="date" placeholder="开始日期" :picker-options="pickerOptions0">
    </el-date-picker>
    <el-date-picker v-model="param.end_time" type="date" placeholder="结束日期" :picker-options="pickerOptions0">
    </el-date-picker>
    <el-select v-model="param.value" placeholder="请选择">
      <!--<el-option v-for="item in options" :label="item.label" :value="item.value">
      </el-option>-->
    </el-select>
    <el-input placeholder="姓名" v-model="param.name">
    </el-input>
    <el-button type="default" class="fa fa-refresh" @click="refresh_data"></el-button>
    <el-button type="primary" class="r fa fa-share-square-o" @click="saveExcel"></el-button>
    <el-input placeholder="搜索" class="right_search" icon="search" v-model="input2" @click="handleIconClick" @keyup.enter.native="handleIconClick">
    </el-input>
    <el-table :data="tableData" border style="width: 100%" height="920">
      <el-table-column fixed :context="_self" inline-template label="操作" width="150">
        <div>
          <el-button size="small" @click="handleEdit($index, row)">
            编辑
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete($index, row)">
            删除
          </el-button>
        </div>
      </el-table-column>
      <el-table-column prop="name" :label=tableHead.name width="120">
      </el-table-column>
      <el-table-column prop="group_name" :label=tableHead.group_name width="120">
      </el-table-column>
      
    </el-table>
    <div class="block">
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="tablePage" :page-sizes="[20, 50, 100, 200, 400]"
        :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="totalNum">
        </el-pagination>
    </div>
  </div>
</template>
<script>
  import {
    excel,
    json2url,
    Vue,
    deepCopyOfObject
  } from "../../../assets/js/util.js"

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
        tableHead: {
          "name": "CI模型名称",
          group_name:"CI模型分组名称",
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

        CICategory: {
          "name": "",
          "id": "",
          group: "",
          structure: {
            // default: [],
            hidden: {
              default: false
            }
          },
        },
        tmp_key: "",
        tmp_name: "",
        tmp_group: "default",
        field_list: {},
        fields_comment: {},
        field: "",
        cpg_list: {
          default: ""
        },
        group_list: {},
        group_name_list: {}
      }
    },

    beforeMount: function () {
      this.get_group_list()
      this.get_field_list()
      
    },
    methods: {
      get_group_list() {
        var query = ""
        this.$http.get("/api/groups/" + query).then((response) => {
          if (response.status !== 200) {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          }
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
      fetch() {
        // console.log(this.param);
        var query = json2url(this.param)
        this.$http.get("/api/items_categories/?" + query).then((response) => {
          if (response.status !== 200) {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          }
          var res = response.data
          for (var key in res) {
            res[key].group_name = this.group_name_list[res[key].group];
            console.log(this.group_name_list);
            
          }
          
          this.tableData1 = res
          this.tableData = this.tableData1.slice(0, this.pageSize)
          this.totalNum = this.tableData1.length
        }, (response) => {
          this.$message({
            type: 'info',
            message: '请求失败, 请重试'
          });
        });
      },
     
      handleEdit(index, row) {
        row.structure['hidden'] = {}
        for (var key in row.structure) {
          row.structure['hidden'][key] = false;
          if (key != "hidden") {
            this.cpg_list[key] = ""
          }
        }
        this.CICategory = deepCopyOfObject(row)
        this.dialogFormVisible = true
        // console.log(index, row);
      },
      createNewCategory() {
        this.dialogFormVisible = true
        this.CICategory = {
          "name": "",
          "id": "",
          group: this.group_list.default,
          structure: {
            // default: [],
            hidden: {
              default: false
            }
          },
        }
      },
      handleDelete(index, row) {
        console.log(index, row);
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
        if (this.CICategory.structure['hidden'][e]) {
          this.CICategory.structure['hidden'][e] = false
        } else {
          this.CICategory.structure['hidden'][e] = true
        }
      }
    }
  }
</script>
<style scoped>
  @import '../../../assets/css/normalize.css';
  @import '../../../assets/css/index.css';
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