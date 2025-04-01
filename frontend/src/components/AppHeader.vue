<template>
  <v-app-bar app color="surface" flat density="comfortable" class="app-header">
    <v-img
      src="@/assets/logo.png"  
      max-height="40"
      max-width="40"
      contain
      class="ml-4 mr-2 app-logo"
      alt="App Logo"
    ></v-img>
    <v-app-bar-title class="app-title">
      <span class="font-weight-bold">美味秘籍</span>
    </v-app-bar-title>

    <v-spacer></v-spacer>

    <!-- Use icon buttons directly on larger screens now -->
    <v-btn icon to="/random" class="header-button d-none d-sm-flex">
      <v-icon>mdi-dice-5-outline</v-icon>
    </v-btn>
    <v-btn icon to="/menu" class="header-button d-none d-sm-flex">
       <v-icon>mdi-silverware-fork-knife</v-icon>
    </v-btn>

    <!-- Buttons for smaller screens (already icons) -->
     <v-btn icon to="/random" class="d-sm-none mx-1"> <!-- Added horizontal margin -->
       <v-icon>mdi-dice-5-outline</v-icon>
     </v-btn>
     <v-btn icon to="/menu" class="d-sm-none mx-1"> <!-- Added horizontal margin -->
       <v-icon>mdi-silverware-fork-knife</v-icon>
     </v-btn>

    <v-menu offset-y>
      <template v-slot:activator="{ props }">
        <v-btn text v-bind="props" class="user-menu-button ml-2 mr-2">
          <v-avatar color="primary" size="32" class="mr-2">
            <!-- Use initials or a user icon -->
            <span class="white--text text-caption">用户</span>
            <!-- Or <v-icon dark>mdi-account-circle</v-icon> -->
          </v-avatar>
          <span class="d-none d-md-inline">用户名</span> 
          <v-icon right class="d-none d-md-inline ml-1">mdi-chevron-down</v-icon>
        </v-btn>
      </template>
      <v-list density="compact" nav>
        <v-list-item link @click="() => {}">
          <template v-slot:prepend>
            <v-icon>mdi-account-circle-outline</v-icon>
          </template>
          <v-list-item-title>个人中心</v-list-item-title>
        </v-list-item>
        <v-list-item link @click="() => {}">
           <template v-slot:prepend>
             <v-icon>mdi-cog-outline</v-icon>
           </template>
          <v-list-item-title>设置</v-list-item-title>
        </v-list-item>
        <v-divider class="my-1"></v-divider>
        <v-list-item link @click="() => {}">
           <template v-slot:prepend>
             <v-icon color="error">mdi-logout</v-icon>
           </template>
          <v-list-item-title class="text-error">退出登录</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

  </v-app-bar>
</template>

<script setup>
// No specific script needed for this header component yet
</script>

<style scoped>
@import '@/assets/components/app-header.css';
</style>
