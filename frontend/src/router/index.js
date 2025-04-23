import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    redirect: '/dashboard',

    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'patients',
        name: 'Patients',
        component: () => import('../views/PatientList.vue'),
        meta: { title: '患者管理' }
      },
      {
        path: 'patients/add',
        name: 'AddPatient',
        component: () => import('../views/PatientForm.vue'),
        meta: { title: '新增患者' }
      },
      {
        path: 'patients/edit/:id',
        name: 'EditPatient',
        component: () => import('../views/PatientForm.vue'),
        meta: { title: '编辑患者' }
      },
      {
        path: 'doctors',
        name: 'Doctors',
        component: () => import('../views/DoctorList.vue'),
        meta: { title: '医师管理' }
      },
      {
        path: 'doctors/add',
        name: 'AddDoctor',
        component: () => import('../views/DoctorForm.vue'),
        meta: { title: '新增医师' }
      },
      {
        path: 'doctors/edit/:id',
        name: 'EditDoctor',
        component: () => import('../views/DoctorForm.vue'),
        meta: { title: '编辑医师' }
      },
      {
        path: 'departments',
        name: 'Departments',
        component: () => import('../views/DepartmentList.vue'),
        meta: { title: '科室管理' }
      },
      {
        path: 'departments/add',
        name: 'AddDepartment',
        component: () => import('../views/DepartmentForm.vue'),
        meta: { title: '新增科室' }
      },
      {
        path: 'departments/edit/:id',
        name: 'EditDepartment',
        component: () => import('../views/DepartmentForm.vue'),
        meta: { title: '编辑科室' }
      },
      {
        path: 'wards',
        name: 'Wards',
        component: () => import('../views/WardList.vue'),
        meta: { title: '病房管理' }
      },
      {
        path: 'wards/add',
        name: 'AddWard',
        component: () => import('../views/WardForm.vue'),
        meta: { title: '新增病房' }
      },
      {
        path: 'wards/edit/:id',
        name: 'EditWard',
        component: () => import('../views/WardForm.vue'),
        meta: { title: '编辑病房' }
      },
      {
        path: 'visits',
        name: 'Visits',
        component: () => import('../views/VisitList.vue'),
        meta: { title: '就诊记录' }
      },
      {
        path: 'visits/add',
        name: 'AddVisit',
        component: () => import('../views/VisitForm.vue'),
        meta: { title: '新增就诊记录' }
      },
      {
        path: 'visits/details/:id',
        name: 'VisitDetail',
        component: () => import('../views/VisitDetail.vue'),
        meta: { title: '就诊记录详情' }
      },
      {
        path: 'admissions',
        name: 'Admissions',
        component: () => import('../views/AdmissionList.vue'),
        meta: { title: '在院患者' }
      },
      {
        path: 'admissions/add',
        name: 'AddAdmission',
        component: () => import('../views/AdmissionAdd.vue'),
        meta: { title: '办理入院' }
      },
      {
        path: 'statistics/department',
        name: 'DepartmentStats',
        component: () => import('../views/DepartmentStats.vue'),
        meta: { title: '科室统计' }
      },
      {
        path: 'statistics/revenue',
        name: 'RevenueStats',
        component: () => import('../views/RevenueStats.vue'),
        meta: { title: '流水统计' }
      },
      {
        path: 'statistics/doctor',
        name: 'DoctorWorkload',
        component: () => import('../views/DoctorWorkload.vue'),
        meta: { title: '医师工作量' }
      },
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 医院管理系统` : '医院管理系统'
  next()
})

export default router 