<template>
  <div class="predict">
    <el-form @submit.prevent="handlePredict">
      <el-form-item label="日期类型">
        <el-select v-model="date_type" placeholder="Select">
          <el-option label="工作日" value="1"></el-option>
          <el-option label="周末" value="2"></el-option>
          <el-option label="节假日" value="3"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="天气情况">
        <el-select v-model="weather_condition" placeholder="Select">
          <el-option label="晴朗" value="1"></el-option>
          <el-option label="多云" value="2"></el-option>
          <el-option label="阴天" value="3"></el-option>
          <el-option label="雨天" value="4"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="室外温度">
        <el-input v-model="temperature" placeholder="Temperature" type="number"></el-input>
      </el-form-item>
      <el-form-item label="促销活动">
        <el-select v-model="promotion" placeholder="Select">
          <el-option label="原价" value="1"></el-option>
          <el-option label="促销" value="2"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handlePredict">Predict</el-button>
      </el-form-item>
    </el-form>
    <div v-if="predictedVisitors !== null">
      Predicted number of visitors: {{ predictedVisitors }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      date_type: '',
      weather_condition: '',
      temperature: '',
      promotion: '',
      predictedVisitors: null
    };
  },
  methods: {
    async handlePredict() {
      try {
        const response = await axios.post('/api/predict/', {
          date_type: Number(this.date_type),
          weather_condition: Number(this.weather_condition),
          temperature: Number(this.temperature),
          promotion: Number(this.promotion)
        });
        this.predictedVisitors = response.data.visitors;
      } catch (error) {
        console.error('Prediction error:', error);
        this.$message.error('Prediction error');
      }
    }
  }
};
</script>

<style scoped>
.predict {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #eaeaea;
  border-radius: 4px;
}
</style>
