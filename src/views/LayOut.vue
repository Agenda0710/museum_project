<template>
  <div>
    <el-container>
      <el-header style="font-size:40px; background-color: rgb(238, 241, 246)">文物保护系统</el-header>

      <el-container>
        <el-aside width="230px" style="border: 1px solid #eee" height="100%">
          <el-menu :default-openeds="['1', '5']">
            <el-submenu index="1">
              <template slot="title"><i class="el-icon-message"></i>博物馆管理</template>
              <el-menu-item-group>
                <router-link to="/eastMuseum" class="router-link">
                  <el-menu-item index="1-1">上海博物馆（东馆）</el-menu-item>
                </router-link>
                <router-link to="/peopleMuseum" class="router-link">
                  <el-menu-item index="1-2">上海博物馆（人广）</el-menu-item>
                </router-link>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="2">
              <template slot="title"><i class="el-icon-menu"></i>文物管理</template>
              <el-menu-item-group>
                <router-link to="/getAllRelics" class="router-link">
                  <el-menu-item index="2-1">文物查询</el-menu-item>
                </router-link>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="3">
              <template slot="title"><i class="el-icon-s-check"></i>用户管理</template>
              <router-link to="/users" class="router-link">
                <el-menu-item index="3-1">用户查询</el-menu-item>
              </router-link>
            </el-submenu>
            <el-submenu index="4">
              <template slot="title"><i class="el-icon-edit"></i>分类管理
              </template>
              <router-link to="/category" class="router-link">
                <el-menu-item index="4-1">文物分类</el-menu-item>
              </router-link>
            </el-submenu>
            <el-submenu index="5">
              <template slot="title"><i class="el-icon-full-screen"></i>工作台显示
              </template>
              <el-menu-item-group>
                <router-link to="/testChart" class="router-link">
                  <el-menu-item index="5-1">大屏展示</el-menu-item>
                </router-link>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="5">
              <template slot="title"><i class="el-icon-s-claim"></i>预测功能
              </template>
              <el-menu-item-group>
                <router-link to="/peoplePrediction" class="router-link">
                  <el-menu-item index="5-1">博物馆人数预测</el-menu-item>
                </router-link>
              </el-menu-item-group>
            </el-submenu>
          </el-menu>
        </el-aside>

        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "LayOut",
  data() {
    return {}
  },
  methods: {}
}
</script>

<style scoped>
.router-link {
  text-decoration: none;
  color: inherit;
}

.router-link .el-menu-item {
  display: block;
}
</style>