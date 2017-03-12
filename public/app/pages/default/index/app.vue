<template>
  <div class="" class="height_100">
    <el-menu theme="dark" default-active="1" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="/model?1">OpenCMDB</el-menu-item>
      <el-submenu index="2">
        <template slot="title">我的工作台</template>
        <el-menu-item index="/model?11">选项1</el-menu-item>
        <el-menu-item index="/model?12">选项2</el-menu-item>
        <el-menu-item index="/model?13">选项3</el-menu-item>
      </el-submenu>
      <el-submenu index="x" class="nav-cap">
        <template slot="title">选项</template>
        <el-menu-item :index="urls.logout">退出</el-menu-item>
        <el-menu-item :index="urls.changepassword">修改密码</el-menu-item>
      </el-submenu>
      <div class="nav-user">
        <span>欢迎 管理员，{{admin_user}}！</span>
      </div>
    </el-menu>
    <el-row class="tac height_100" :gutter="20">
      <el-col :span="4">
        <el-menu mode="vertical" :default-active="path" class="el-menu-vertical-demo" @select="handleSelect" router>
          <el-menu-item index="/model"><i class="fa fa-cogs"></i> 模型</el-menu-item>
          <el-menu-item index="/barn/"><i class="fa fa-cogs"></i> 仓库</el-menu-item>
          <el-menu-item index="/storage"><i class="fa fa-cogs"></i> 应用</el-menu-item>
          <!--</el-menu-item-group>-->
        </el-menu>
      </el-col>
      <el-col :span=20 class="height_100">
        <el-breadcrumb separator="/" class="breadcrumb_padding">
          <el-breadcrumb-item>首页</el-breadcrumb-item>
          <el-breadcrumb-item>{{breadcrumb1}}</el-breadcrumb-item>
          <el-breadcrumb-item>{{breadcrumb2}}</el-breadcrumb-item>
        </el-breadcrumb>
        <!--<iframe id="checkListFrame1" class="height_100" src="/model" frameborder="0" width="100%" height="90%" scrolling="auto"></iframe>-->
        <router-view></router-view>
      </el-col>
    </el-row>
    <!--<div id="footer">
      <hr>
      <footer class="text-center">
        <p>© 我的公司</p>
      </footer>
    </div>-->
  </div>
</template>
<script>
  export default {
    data() {
      return {
        breadcrumb1: "dashboard",
        breadcrumb2: "",
        urls: {
          logout: "/default/login.html",
          changepassword: "/admin/manage/password"
        },
        admin_user: "",
        menus1: {},
        path: "",
      }
    },
    mounted: function () {
      window.vm = this;
      this.path = this.$route.path

      this.$http.get("/api/current_user/").then((response) => {
        this.admin_user = response.data.realname ? response.data.realname : response.data.username
        this.form = response.data
      }, (response) => {
        this.$message({
          type: 'info',
          message: '请求失败, 请重试'
        });
      });
    },
    methods: {
      handleSelect(key, keyPath) {
        if (key == this.urls.logout) {
          localStorage.setItem("Authorization", '')
          location.href = key;
          return;
        }
        // this.breadcrumb1 = this.menus1[keyPath[0]]['text']
        // this.breadcrumb2 = this.menus1[keyPath[0]][keyPath[1]]['text']
      },
      handleOpen(key, keyPath) {},
      show_error_message(msg) {
        this.$message({
          type: 'error',
          message: msg || "请求失败, 请检查数据(重名)并重试",
          showClose: true,
          // duration: 5,
        });
        if (msg == "Signature has expired.") {
          localStorage.setItem("Authorization", '')
          setTimeout(function () {
            parent.document.location.href = "/default/login.html"
          }, 500);
          return
        }
      },
    },
  }
</script>
<style scoped>
  @import '../../../assets/css/normalize.css';
  @import '../../../assets/css/index.css';
  body {
    font-family: Helvetica, sans-serif;
  }
  
  .new_btn {
    margin-left: -70px;
    left: 50%;
    position: relative;
    margin-bottom: 3px;
  }
  
  .edit_mini_btn {
    background: transparent;
    border: navajowhite;
  }
  
  .nav-cap {
    font-size: 18;
    float: right!important;
  }
  
  .nav-user {
    display: inline;
    color: aliceblue;
    float: right;
    margin-right: 20px;
    position: relative;
    margin-top: 17px;
  }
</style>
