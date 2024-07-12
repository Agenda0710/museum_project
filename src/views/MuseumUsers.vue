<template>
  <div>
    <el-table :data="users" style="width: 100%">
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="user_name" label="用户名"></el-table-column>
      <el-table-column prop="gender" label="性别">
        <template slot-scope="scope">
          <span>{{ scope.row.gender === 1 ? "男性" : "女性" }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="birthday" label="生日"></el-table-column>
      <el-table-column prop="status" label="账号状态">
        <template slot-scope="scope">
          <span>{{ scope.row.status === 1 ? "启用" : "禁用" }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="position" label="职位">
        <template slot-scope="scope">
          <span>{{ scope.row.position === 1 ? "管理员" : "普通用户" }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: []
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      axios.get('/api/getAllUsers/')
          .then(response => {
            this.users = response.data;
          })
          .catch(error => {
            console.error('Error fetching users:', error);
          });
    },
  }
};
</script>

<style scoped>
.el-table {
  margin: 20px 0;
}
</style>
