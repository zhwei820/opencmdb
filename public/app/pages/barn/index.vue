<template>
  <div class="height_100">
    <!--<el-menu theme="dark" default-active="1" class="el-menu-demo" mode="horizontal">
      <el-menu-item index="1">CMDB管理中心</el-menu-item>
    </el-menu>-->
    <el-row class="tac height_100">
      <el-col :span="4">
        <el-menu class="el-menu-vertical-demo" @select="handleSelect" @open="handleOpen">
          <el-submenu :index="submenus.uri" v-for="submenus in menus">
            <template slot="title"><i class="fa fa-sitemap"></i> {{submenus.text}}
            </template>
            <!--<el-menu-item :index="submenu.uri" v-for="submenu in submenus.items">{{submenu.text}}</el-menu-item>-->
            <el-submenu :index="submenus1.uri" v-for="submenus1 in submenus.menus">
              <template slot="title"><i class="fa fa-cubes"></i> {{submenus1.text}}
              </template>
              <el-menu-item :index="submenu.uri" v-for="submenu in submenus1.items"><i class="fa fa-cube"> {{submenu.text}}</el-menu-item>
            </el-submenu>
          </el-submenu>
        </el-menu>
      </el-col>
      <!--sidebar end-->
      <el-col :span=20 class="height_100">
        <el-breadcrumb separator="/" class="breadcrumb_padding">
        </el-breadcrumb>
        <!--<router-view></router-view>-->
        <items :category-id="id"> </items>

      </el-col>
    </el-row>

  </div>
</template>
<script>
  import {
    addEvent
  } from "../../assets/js/util.js"
  import Items from "./items.vue"

  export default {
    data() {
      return {
        breadcrumb1: "dashboard",
        breadcrumb2: "",
        menus: [],
        id:"",

        // menus: [{
        //   uri: "/",
        //   text: "层",
        //   menus: [{
        //     uri: "/model/layer.html?123",
        //     text: "组",
        //     items: [{
        //       text: "模型",
        //       uri: "/model/layer.html?123",
        //     }, {
        //       text: "模型",
        //       uri: "/model/group.html?1233",
        //     }, {
        //       text: "模型",
        //       uri: "/model/item_category.html?1232",
        //     }, ]
        //   }, {
        //     uri: "/model/group.html?123",
        //     text: "组",
        //     items: [{
        //       text: "模型",
        //       uri: "/model/layer.html?1213",
        //     }, {
        //       text: "模型",
        //       uri: "/model/group.html?12313",
        //     }, {
        //       text: "模型",
        //       uri: "/model/item_category.html?12132",
        //     }, ]
        //   }],
        // }],
        menus1: {},
      }
    },
    components:{
      items:Items,
    },

    beforeMount: function () {
      var id = this.$route.params.id
      this.id = id == undefined ? "" : id
      // this.id = "58953a76cc8b7914090dea76"
      this.get_model_menus()
      window.vm = this
    },
    methods: {
      get_model_menus() {
        var that = this
        var layer_list, layer_name_list
        var p1 = new Promise(
          function (resolve, reject) {
            that.get_model_data("/api/layers/", "", resolve, reject)
          }
        );

        var group_list, group_name_list, group_by_list_of_group
        var p2 = new Promise(
          function (resolve, reject) {
            that.get_model_data("/api/groups/", "layer", resolve, reject)
          }
        );

        var item_category_list, item_category_name_list, group_by_list_of_item_category
        var p3 = new Promise(
          function (resolve, reject) {
            that.get_model_data("/api/items_categories/", "group", resolve, reject)
          }
        );

        p1.then((res) => {
          layer_list = res[0];
          layer_name_list = res[1]
          // console.log(layer_name_list)
          return p2 // 黑科技!
        }).then((res) => {
          group_list = res[0];
          group_name_list = res[1]
          group_by_list_of_group = res[2]
          // console.log(group_name_list)
          return p3
        }).then((res) => {
          item_category_list = res[0];
          item_category_name_list = res[1]
          group_by_list_of_item_category = res[2]
          // console.log(item_category_name_list)
          this.menus = []
          for (var key in layer_name_list) {
            var element = layer_name_list[key];
            var m1 = {
              uri: "/model/layer_edit.html?id=" + key,
              text: element,
              id: key,
              items: []
            }
            var menus1 = []

            for (var key1 in group_by_list_of_group[key]) {
              var element1 = group_by_list_of_group[key][key1];

              var menus2 = {};
              menus2.uri = "/model/group_edit.html?id=" + element1.id
              menus2.text = element1.name
              menus2.id = element1.id
              menus2.items = []
              for (var key2 in group_by_list_of_item_category[element1.id]) {
                var element2 = group_by_list_of_item_category[element1.id][key2];
                var menu_item = {}
                menu_item.uri = element2.id
                menu_item.text = element2.name

                menu_item.route = { path: '/items/' + element2.id}

                menus2.id = element1.id
                menus2.items.push(menu_item)
              }
              menus1.push(menus2)
            }
            m1.menus = menus1;
            this.menus.push(m1)
          }

        })

      },
      get_model_data(url, group_by, resolve, reject) {
        var query = ""
        var list, name_list, group_by_list
        this.$http.get(url + query).then((response) => {
          if (response.status !== 200) {
            this.$message({
              type: 'info',
              message: '请求失败, 请重试'
            });
          }
          list = {}
          for (var key in response.data) {
            list[response.data[key].name] = response.data[key].id;
          }
          name_list = {}
          for (var key in response.data) {
            name_list[response.data[key].id] = response.data[key].name;
          }

          group_by_list = {}
          if (group_by) {
            for (var key in response.data) {
              if (group_by_list[response.data[key][group_by]] == undefined) {
                group_by_list[response.data[key][group_by]] = []
              }
              group_by_list[response.data[key][group_by]].push(response.data[key]);
            }
          }
          resolve([list, name_list, group_by_list])
        }, (response) => {
            var msg = response.data.detail != undefined ? response.data.detail : response.data.error
            parent.vm.show_error_message(msg)

          // reject()
        });
      },
      handleSelect(key, keyPath) {
        this.id = key
        console.log(this.id)
      },
      handleOpen(key, keyPath) {
        if (key != "/") {
        }
      },
     
      show_error_message(msg){
          // parent.vm.show_error_message(msg)
          this.$message({
            type: 'info',
            message: msg
          });
      },
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