<template>
  <div id="app">
    <div id="loginContainer">
      <img v-bind:src="logoImg" width="100px">
      <h1>{{ msg }}</h1>
      <div id="loginForm">
        <el-form :model="ruleForm" ref="ruleForm" label-width="120px" class="demo-ruleForm">
          <el-form-item class="inputContainer" label="username" prop="username">
            <el-input v-model="ruleForm.username"></el-input>
          </el-form-item>
          <el-form-item class="inputContainer" label="password" prop="password">
            <el-input type="password" v-model="ruleForm.password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" id="loginSubmitButton" @click="login">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script>
  import logo from 'assets/img/logo.png'
  export default {
    data() {
      return {
        msg: 'OpenCMDB管理系统',
        logoImg: logo,

        ruleForm: {
          username: "",
          password: "",
        },
      }
    },

    methods: {
      startHacking() {
        this.$notify({
          title: 'It Works',
          message: 'We have laid the groundwork for you. Now it\'s your time to build something epic!',
          duration: 6000
        })
      },
      login() {
        this.$http.post("/api/api-token-auth/?", this.ruleForm).then((response) => {
            localStorage.setItem("Authorization", "JWT " + response.data['token'])
            if (response.status !== 200) {
              this.$message({
                type: 'info',
                message: '请求失败, 请重试'
              });
            } else {
              this.$message({
                type: 'info',
                message: '登录成功'
              });
              location.href = "/default/index.html"
            }
          },
          (response) => {
            this.$message({
              type: 'info',
              message: '登录失败'
            });
          }
        );
      }

    }
  }
</script>
<style>
  body {
    font-family: Helvetica, sans-serif;
  }
  
  #loginContainer {
    width: 80%;
    max-width: 540px;
    min-width: 300px;
    margin: auto;
    background-color: #fff;
    text-align: center;
    padding-bottom: 3.5em;
    border-radius: 1em;
    margin-top: 15%;
  }
  
  #title {
    padding-top: 3em;
    margin-bottom: 2.5em;
  }
  
  #title .text {
    font-size: 1.5em;
    color: #333;
  }
  
  #loginForm {
    font-size: 1em;
  }
  
  #loginError {
    /* display: none; */
    text-align: left;
    color: red;
    width: 22.36em;
    margin: 1em auto;
  }
  
  .inputContainer {
    margin-bottom: 1.43em;
  }
  
  .inputContainer input {
    font-size: 1em;
    height: 2.93em;
    width: 80%;
    max-width: 352px;
    min-width: 250px;
    background-color: rgb(250, 250, 250);
    border: solid 1px #eee;
    border-radius: 0.21em;
    padding-left: 0.5em;
  }
  
  #loginSubmitButton {
    cursor: pointer;
    font-size: 1em;
    width: 80%;
    max-width: 352px;
    min-width: 250px;
    height: 2.71em;
    color: #fff;
    background-color: #3caf33;
    border-radius: 1.29em;
    margin-top: 1.43em;
    margin-right: 120px;
  }
  
  input,
  button {
    border: none;
    outline: none;
    background: none;
  }
  
  body {
    background: #d2d6de;
  }
</style>
