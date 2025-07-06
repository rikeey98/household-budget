import { defineStore } from 'pinia';
import { login, logout, getCurrentUser } from 'src/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
  }),
  actions: {
    async loginAction(username, password) {
      this.loading = true;
      this.error = null;
      try {
        await login(username, password);
        const res = await getCurrentUser();
        this.user = res.data;
        this.isAuthenticated = true;
      } catch {
        this.error = '로그인 실패: 아이디 또는 비밀번호를 확인하세요.';
        this.user = null;
        this.isAuthenticated = false;
      } finally {
        this.loading = false;
      }
    },
    async logoutAction() {
      this.loading = true;
      this.error = null;
      try {
        await logout();
        this.user = null;
        this.isAuthenticated = false;
      } catch {
        this.error = '로그아웃 실패';
      } finally {
        this.loading = false;
      }
    },
    async fetchUser() {
      this.loading = true;
      this.error = null;
      try {
        const res = await getCurrentUser();
        this.user = res.data;
        this.isAuthenticated = true;
      } catch {
        this.user = null;
        this.isAuthenticated = false;
      } finally {
        this.loading = false;
      }
    }
  }
}); 