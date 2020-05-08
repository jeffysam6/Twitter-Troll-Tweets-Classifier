<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    {{this.$route.params.username}}

    <template v-if="tweets">
  <el-table
    :data="tweets"
    style="width: 100%">
    <el-table-column
      prop="id"
      label="Id"
      width="180">
    </el-table-column>
    <!-- <el-table-column
      prop="username"
      label="Username"
      width="180">
    <router-link :to="{name: 'Profile', params: {username: username}}">
         
    </router-link>
    </el-table-column> -->
    <el-table-column
      prop="tweet"
      label="Tweet">
    </el-table-column>
    <el-table-column
      prop="is_troll"
      label="Is Troll?">
    </el-table-column>
  </el-table>
    </template>
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import { Component, Vue } from 'vue-property-decorator';
import axios from "axios";
import {server} from "../utils/helper";

@Component({
 name: 'ProfileComponent',
  components: {
  }
})

export default class extends Vue {
  private tweets = [];


  created() 
  {
    this.fetchTweets();
    console.log(this.tweets)

  }

  private fetchTweets() {
    axios
    .get(`${server.baseURL}/user?username=${this.$route.params.username}`)
    .then((data: any) => {this.tweets = data.data;})
  }

}


</script>

<style>

.el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }


</style>