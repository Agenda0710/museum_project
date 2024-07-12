<template>
  <div class="login">
    <el-form @submit.prevent="handleLogin">
      <el-form-item label="Username">
        <el-input v-model="username" placeholder="Username"></el-input>
      </el-form-item>
      <el-form-item label="Password">
        <el-input type="password" v-model="password" placeholder="Password"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="changeView">Login</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async handleLogin() {
      console.log('Attempting to log in');
      try {
        const response = await axios.post('/api/login/', {
          username: this.username,
          password: this.password
        });
        console.log('Login successful:', response.data);
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
      } catch (error) {
        console.error('Login error:', error);
        this.$message.error('Invalid credentials');
      }
    },
    changeView() {
      this.$router.push('/eastMuseum');
    }
  }
};
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #eaeaea;
  border-radius: 4px;
}
</style>
