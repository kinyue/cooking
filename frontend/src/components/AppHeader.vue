<template>
  <v-app-bar app color="primary" dark>
    <v-toolbar-title class="text-h5 font-weight-bold">
      <v-img
        src="/logo.png"
        max-height="30"
        max-width="30"
        contain
        class="mr-2"
      />
      美味秘籍
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn text class="mr-2">
      随机看看 <v-icon right>mdi-dice-5</v-icon>
    </v-btn>

    <v-btn text class="mr-2">
      今日菜单 <v-icon right>mdi-calendar-today</v-icon>
    </v-btn>

    <v-menu bottom offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          v-bind="attrs"
          v-on="on"
          text
        >
          <v-avatar size="32" class="mr-2">
            <v-icon>mdi-account-circle</v-icon>
          </v-avatar>
          用戶
        </v-btn>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title>设置</v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>登出</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      searchQuery: null,
    };
  },
};
</script>

<style scoped>
</style>
