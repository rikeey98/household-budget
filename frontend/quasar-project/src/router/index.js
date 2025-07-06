import { defineRouter } from '#q-app/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'src/stores/auth';
import { getActivePinia, setActivePinia, createPinia } from 'pinia';

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  // 인증 가드 추가
  Router.beforeEach(async (to, from, next) => {
    // Pinia 인스턴스가 없으면 생성 및 활성화
    if (!getActivePinia()) {
      setActivePinia(createPinia())
    }
    const auth = useAuthStore();
    // 인증 상태가 초기화되지 않은 경우(새로고침 등) fetchUser로 동기화
    if (auth.isAuthenticated === false && !auth.user) {
      await auth.fetchUser();
    }
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!auth.isAuthenticated) {
        next({ path: '/login', query: { redirect: to.fullPath } });
      } else {
        next();
      }
    } else {
      next();
    }
  });

  return Router
})
