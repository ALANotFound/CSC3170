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
    // 检查HTTP状态码是否在200-299范围内
    if (response.status >= 200 && response.status < 300) {
      return response.data
    }
    
    const res = response.data
    
    // 如果后端返回了错误信息，显示错误
    if (res.message && res.message !== 'success') {
      ElMessage({
        message: res.message,
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
      
      return Promise.reject(new Error(res.message))
    }
    
    return Promise.reject(new Error('请求失败'))
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