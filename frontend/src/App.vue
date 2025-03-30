<template>
  <v-app>
    <v-app-bar app color="surface" flat density="comfortable">
      <v-img
        src="/path/to/your/logo.png"  
        max-height="40"
        max-width="40"
        contain
        class="ml-4 mr-2"
      ></v-img>
      <v-app-bar-title>
        <span class="font-weight-bold">美味秘籍</span>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn text to="/random">随机看看</v-btn>
      <v-btn text to="/menu">今日菜单</v-btn> 

      <v-menu offset-y>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props" class="ml-4 mr-4">
            <v-avatar color="grey lighten-2" size="36">
              <v-icon icon="mdi-account"></v-icon>
              </v-avatar>
             <span class="ml-2 d-none d-sm-inline">用户名</span>
             <v-icon right class="ml-1 d-none d-sm-inline">mdi-chevron-down</v-icon>
          </v-btn>
        </template>
        <v-list density="compact">
          <v-list-item @click="() => {}"> 
            <v-list-item-title>个人中心</v-list-item-title>
          </v-list-item>
          <v-list-item @click="() => {}">
            <v-list-item-title>设置</v-list-item-title>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="() => {}">
            <v-list-item-title>退出登录</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
// No specific script needed for this basic layout
</script>

<style scoped>
/* Optional: Scoped styles for App.vue */
.v-main {
  /* Use the background color from the theme */
  background-color: rgb(var(--v-theme-background));
}
.v-app-bar-title {
  flex-grow: 0; /* Prevent title from taking too much space */
  min-width: 100px; /* Adjust as needed */
}
.v-btn {
  text-transform: none; /* Prevent buttons from being all caps */
}
/* Adjust user name visibility */
@media (max-width: 600px) {
  .d-sm-inline {
     display: none !important;
  }
   .v-btn.ml-4.mr-4 { /* Reduce spacing around avatar on mobile */
     margin-left: 8px !important;
     margin-right: 8px !important;
   }
}
</style>