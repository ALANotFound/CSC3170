import request from '@/utils/request'

// 获取科室统计数据
export function getDepartmentStats(id, params) {
  return request({
    url: `/department/${id}/stats`,
    method: 'get',
    params
  })
}

// 获取收入统计数据
export function getRevenueStats(params) {
  return request({
    url: '/report/revenue',
    method: 'get',
    params
  })
}

// 获取医师工作量统计数据
export function getDoctorWorkload(id, params) {
  return request({
    url: `/doctor/${id}/workload`,
    method: 'get',
    params
  })
} 