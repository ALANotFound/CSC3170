import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://127.0.0.1:5000', // 本地后端API的基础URL
  timeout: 10000 // 请求超时时间
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 如果后端约定的状态码不是200或201，说明请求出错
    if (res.code !== 200 && res.code !== 201) {
      ElMessage({
        message: res.message || '请求失败',
        type: 'error',
        duration: 5 * 1000
      })
      
      // 401: 未登录或token过期
      if (res.code === 401) {
        // 提示用户重新登录
        ElMessage({
          message: '登录已过期，请重新登录',
          type: 'error',
          duration: 5 * 1000,
          onClose: () => {
            localStorage.removeItem('token')
            router.push('/login')
          }
        })
      }
      
      return Promise.reject(new Error(res.message || '请求失败'))
    } else {
      return res
    }
  },
  error => {
    console.error('响应错误:', error)
    ElMessage({
      message: error.message || '请求失败',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service 