<template>
  <div class="bg">
    <dv-border-box-11 title="数据中心" style="width: 100%;height: 45rem">
      <dv-full-screen-container>
        <div class="naca">
          <div class="left">
            <div class="left-1">
              <dv-border-box-8>
                <!-- 左下 编号6 水位 -->
                <dv-water-level-pond :config="eastPercent" style="width:350px;height:200px"/>
                <dv-decoration-8 style="width:350px;height:20px;"/>
              </dv-border-box-8>
            </div>
            <div class="left-1">
              <dv-border-box-10>
                <!-- 左中 编号7  电量 -->
                <dv-percent-pond :config="peoplePercent" style="width:350px;height:200px;"/>
                <dv-decoration-1 style="width:350px;height:10px;"/>
              </dv-border-box-10>

            </div>
            <div class="left-1">
              <!-- 左上 -->
              <dv-decoration-9 style="width:350px;height:200px">
                <dv-decoration-11 style="width:200px;height:60px;">东馆，人广文物展出</dv-decoration-11>
              </dv-decoration-9>
            </div>
          </div>
          <div class="cents">
            <div class="cent">
              <dv-border-box-1>
                <!-- 流动表格 编号3 中上 -->
                <dv-scroll-board :config="tableData" style="width:700px;height:100%"/>
                <dv-decoration-5 style="width:700px;height:10px;"/>
              </dv-border-box-1>
            </div>
            <div class="cent-1">
              <dv-border-box-10>
                <!-- 排名 编号4 中下 -->
                <!--                <dv-capsule-chart :config="ColumChartInfo" style="width:95%;height:100%"/>-->
                <dv-scroll-ranking-board :config="activeCircle" style="width:99%;height:95%"/>
              </dv-border-box-10>
            </div>
          </div>
          <div class="left">
            <!--            <div class="left-1">-->
            <!--              <dv-border-box-1>-->
            <!--                &lt;!&ndash; 小飞机 编号4  右下 &ndash;&gt;-->

            <!--                <dv-decoration-8 :reverse="true" style="width:350px;height:20px;"/>-->
            <!--              </dv-border-box-1>-->
            <!--            </div>-->
            <div class="left-1">
              <!-- 右下 -->
              <dv-decoration-12 style="width:330px;height:220px;">
                <dv-active-ring-chart :config="activeCircle" style="width:330px;height:220px"/>
              </dv-decoration-12>
            </div>
            <br>
            <div class="left-1">
              <dv-capsule-chart :config="ColumChartInfo" style="width:100%;height:100%"/>
              <!-- 流动表格  编号5 右上 -->
              <!--              <dv-scroll-ranking-board :config="activeCircle" style="width:300px;height:250px"/>-->
              <br>

              <dv-decoration-9 style="width:350px;height:10px;"></dv-decoration-9>

            </div>
          </div>
        </div>
      </dv-full-screen-container>
    </dv-border-box-11>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      eastPercent: {
        data: [50]
      },
      peoplePercent: {
        value: 50
      },
      tableData: {
        header: ['文物', '藏馆', '地址'],
        data: []
      },
      activeCircle: {
        data: [
          {
            name: '',
            value: '',
          }
        ]
      },
      ColumChartInfo: {
        data: [
          {
            name: '',
            value: '',
          }
        ]
      }
    };
  },
  created() {
    axios.get("/api/getPercent/?id=1/").then(response => {
      const newData = [response.data.percent];
      this.eastPercent = {...this.eastPercent, data: newData};
    }).catch(error => {
      console.error("Error fetching data:", error);
    });

    axios.get("/api/getPercent/?id=2/").then(response => {
      const newData = response.data.percent;
      this.peoplePercent = {...this.peoplePercent, value: newData};
    }).catch(error => {
      console.error("Error fetching data for peoplePercent:", error);
    });

    axios.get("/api/getRelicsInfo/").then(response => {
      const newData = response.data.map(item => [item.name, item.museumName, item.location]);
      this.tableData = {...this.tableData, data: newData};
    }).catch(error => {
      console.error("Error fetching relics info:", error);
    });

    axios.get("/api/getCircleInfo/").then(response => {
      const newData = response.data.map(item => ({
        name: item.name,
        value: item.count// Assuming count is a number, convert it to string if needed
      }));
      this.activeCircle = {...this.activeCircle, data: newData};
    }).catch(error => {
      console.error("获取圆环图信息时出错:", error);
    });

    axios.get("/api/getColumChartInfo/").then(response => {
      const newData = response.data.map(item => ({
        name: item.name,
        value: item.count// Assuming count is a number, convert it to string if needed
      }));
      this.ColumChartInfo = {...this.ColumChartInfo, data: newData};
    }).catch(error => {
      console.error("获取柱状图信息时出错:", error);
    });
  }
};
</script>

<style>
.cent {
  margin: 10px;
  width: 700px;
  height: 412px;
  /* background-color: blueviolet; */
}

.cent-1 {
  margin: 10px;
  color: aliceblue;
  width: 700px;
  height: 200px;
  /* background-color: rgb(26, 26, 133); */
}

.left {
  display: flex;
  flex-direction: column-reverse;
}

.left-1 {
  margin: 15px;
  color: aliceblue;
  width: 350px;
  height: 50%;
  /* background-color: rgb(26, 26, 133); */
}

.naca {
  width: 100%;
  height: 40rem;
  /* padding: 120px; */
  margin: 80px 24px;
  /* background-color: aquamarine; */
  display: flex;
}

.bg {
  width: 100%;
  height: 45rem;
  background-color: black;
  position: relative;
}
</style>