<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <el-row>
    <el-input
    placeholder="Enter the hashtag"
    v-model="hashtag"
    clearable
    autosize
    autofocus
    >
    </el-input>
    <el-button 
    type="primary"
    v-on:click="fetchTweets">Scrape</el-button>
    </el-row>

    <template v-if="tweets">
  <el-table
    :data="tweets"
    style="width: 100%">
    <el-table-column
      prop="id"
      label="Id"
      width="180">
    </el-table-column>
    <el-table-column
      prop="username"
      label="Username"
      width="180">
       <template slot-scope="scope">
        <router-link :to="{name: 'Profile', params: {username: scope.row.username}}">
          <span>{{ scope.row.username }}</span> 
          </router-link>
        </template>
    </el-table-column>
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
 name: 'Home',
  components: {
  }
})
export default class extends Vue {
  private tweets = [];
  private hashtag = "";


  // created() 
  // {
  //   this.fetchTweets();
  //   console.log(this.tweets)

  // }

  private fetchTweets() {
    axios
    .get(`${server.baseURL}/api?hashtag=${this.hashtag}`)
    .then((data: any) => {this.tweets = data.data;console.log(this.tweets)})
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