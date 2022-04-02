<template>
	<div height="840px" width="800px">
		<el-header style="background-color: #ffffff;margin-left: 25px;margin-right: 25px;border-bottom: 1px solid rgb(28, 202, 213);">
		    <font style="font-family: 'Microsoft YaHei';font-size: 30px;color: #000000;">Account Assets</font>
		</el-header>
		<el-row style="width: 96%;height: 600px; margin-left: 25px;margin-top: 20px">
			<el-col :span="12">
				<div ref="bar_dv1" style="width:100%;height: 600px; margin-left: 25px;margin-top: 20px"></div>
			</el-col>
			<el-col :span="12">
				<div ref="bar_dv2" style="width:100%;height: 600px; margin-left: 25px;margin-top: 20px"></div>
			</el-col>
		</el-row>
	</div>
</template>

<script>
	import echarts from 'echarts'
	export default {
		name: "Account",
		data() {
			return {
				chart1: null,
				chart2: null,
				data1: [
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					}
				],
				data2: [
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					},
					{
						value: null,
						name: null
					}
				]
			}
		},
		created() {
			const _this = this;
			var price = 0.0;
			axios.get('/api/getcount/').then(function (data) {
				console.log(data.data)
				_this.data1[0].value = data.data;
				price += data.data;
				_this.data1[0].name = 'Balance';
			})
			axios.get('/api/getstockprice/?code=000001').then(function (data) {
				console.log(data.data)
				if (data.data != '0.0') {
					_this.data1[1].value = data.data;
					price += data.data;
					_this.data1[1].name = 'Code:000001';
				}
			})
			axios.get('/api/getstockprice/?code=000002').then(function (data) {
				console.log(data.data)
				if (data.data != '0.0') {
					_this.data1[2].value = data.data;
					price += data.data;
					_this.data1[2].name = 'Code:000002';
				}
			})
			axios.get('/api/getstockprice/?code=000003').then(function (data) {
				if (data.data != '0.0') {
					_this.data1[3].value = data.data;
					price += data.data;
					_this.data1[3].name = 'Code:000003';
				}
			})
			axios.get('/api/getstockprice/?code=000004').then(function (data) {
				if (data.data != '0.0') {
					_this.data1[4].value = data.data;
					price += data.data;
					_this.data1[4].name = 'Code:000004';
				}
			})
			axios.get('/api/getstockprice/?code=000005').then(function (data) {
				if (data.data != '0.0') {
					_this.data1[5].value = data.data;
					price += data.data;
					_this.data1[5].name = 'Code:000005';
				}
			})
			axios.get('/api/getstockprice/?code=000006').then(function (data) {
				if (data.data != '0.0') {
					_this.data1[6].value = data.data;
					price += data.data;
					_this.data1[6].name = 'Code:000006';
				}
			})
			axios.get('/api/getstock/?code=000001').then(function (data) {
				_this.data2[0].value = data.data;
				_this.data2[0].name = 'Code:000001';
			})
			axios.get('/api/getstock/?code=000002').then(function (data) {
				_this.data2[1].value = data.data;
				_this.data2[1].name = 'Code:000002';
			})
			axios.get('/api/getstock/?code=000003').then(function (data) {
				_this.data2[2].value = data.data;
				_this.data2[2].name = 'Code:000003';
			})
			axios.get('/api/getstock/?code=000004').then(function (data) {
				_this.data2[3].value = data.data;
				_this.data2[3].name = 'Code:000004';
			})
			axios.get('/api/getstock/?code=000005').then(function (data) {
				_this.data2[4].value = data.data;
				_this.data2[4].name = 'Code:000005';
			})
			axios.get('/api/getstock/?code=000006').then(function (data) {
				_this.data2[5].value = data.data;
				_this.data2[5].name = 'Code:000006';
			})
			setTimeout(() =>{
			    _this.getchart1(price.toFixed(2));
				_this.getchart2();
			}, 10000);
		},
		methods:{
			getchart1(price) {
				this.chart1 = echarts.init(this.$refs.bar_dv1);
				let option = {
					  title: {
						text: 'Proportion of funds held',
						subtext: 'Total Assets: ' + price,
						left: 'center'
					  },
					  tooltip: {
						trigger: 'item'
					  },
					  legend: {
						orient: 'vertical',
						left: 'left'
					  },
					  series: [
						{
						  name: 'Access From',
						  type: 'pie',
						  radius: '50%',
						  data: this.data1,
						  emphasis: {
							itemStyle: {
							  shadowBlur: 10,
							  shadowOffsetX: 0,
							  shadowColor: 'rgba(0, 0, 0, 0.5)'
							}
						  }
						}
					  ]
					};
				this.chart1.setOption(option);
			},
			getchart2() {
				this.chart2 = echarts.init(this.$refs.bar_dv2);
				let option = {
					  title: {
						text: 'Proportion of shares held',
						// subtext: 'Fake Data',
						left: 'center'
					  },
					  tooltip: {
						trigger: 'item'
					  },
					  legend: {
						orient: 'vertical',
						left: 'left'
					  },
					  series: [
						{
						  name: 'Access From',
						  type: 'pie',
						  radius: '50%',
						  data: this.data2,
						  emphasis: {
							itemStyle: {
							  shadowBlur: 10,
							  shadowOffsetX: 0,
							  shadowColor: 'rgba(0, 0, 0, 0.5)'
							}
						  }
						}
					  ]
					};
				this.chart2.setOption(option);
			}
		}
	}
</script>

<style>
</style>
