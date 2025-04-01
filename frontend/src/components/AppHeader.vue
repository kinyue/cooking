<template>
  <v-app-bar app color="surface" flat density="comfortable" class="app-header">
    <v-img
      src="/logo.png"  
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

    <v-btn text to="/random" class="header-button d-none d-sm-flex">
      <v-icon left class="mr-1">mdi-dice-5-outline</v-icon>
      随机看看
    </v-btn>
    <v-btn text to="/menu" class="header-button d-none d-sm-flex">
       <v-icon left class="mr-1">mdi-silverware-fork-knife</v-icon>
       今日菜单
    </v-btn>

    <!-- Buttons for smaller screens -->
     <v-btn icon to="/random" class="d-sm-none">
       <v-icon>mdi-dice-5-outline</v-icon>
     </v-btn>
     <v-btn icon to="/menu" class="d-sm-none">
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
.app-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12) !important; /* Add a subtle border */
}

.app-logo {
  cursor: pointer; /* Indicate logo is clickable (if it links home) */
}

.app-title {
  flex-grow: 0; /* Prevent title from taking too much space */
  min-width: 100px; /* Adjust as needed */
  font-family: 'Roboto', sans-serif; /* Example: Use a specific font */
}

.header-button {
  text-transform: none; /* Prevent buttons from being all caps */
  font-weight: 500;
  letter-spacing: 0.5px;
  margin: 0 4px; /* Add some horizontal margin */
}

.user-menu-button {
   text-transform: none;
   font-weight: 500;
}

/* Adjust user name visibility based on screen size */
/* d-none d-md-inline handles this now in the template */

/* Ensure avatar text is visible */
.v-avatar .white--text {
  color: white !important;
}

/* Style menu items */
.v-list-item {
  min-height: 40px;
}
.v-list-item-title {
  font-size: 0.9rem;
}
.v-list-item .v-icon {
  margin-right: 12px;
}
</style>
