<template>
    <div height="840px" width="800px">
        <el-header justify="end" style="background-color: #ffffff;margin-left: 25px;margin-right: 25px;border-bottom: 1px solid rgb(28, 202, 213);">
            <el-select v-model="value" placeholder="Please select stock code" style="">
                <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                </el-option>
            </el-select>
            <el-button type="primary" @click="query(value)" style="margin-left: 14px">QUERY</el-button>
            <el-button type="primary" @click="dialog = true, getbalance()" style="margin-left: 14px">TRANSCAT</el-button>
        </el-header>
		
		<div  ref="bar_dv"  style="width:95%;height: 600px; margin-left: 25px;margin-top: 20px"></div>
		
		<el-dialog :visible.sync="dialog" style="width: 1000px; margin: auto">
		    <el-form :model="form" style="width: 100%">
		        <el-form-item label="Account Balance" :label-width="formLabelWidth" >
		            <el-input v-model="balance" :disabled="true" style="width: 221.4px;margin-left: 20px"></el-input>
		        </el-form-item>
		        <hr>
		        <el-form-item label="Stock Code"  :label-width=formLabelWidth style="margin-top: 20px">
		            <el-select v-model="code" placeholder="Please Select" style="margin-left: 20px">
		                <el-option
		                        v-for="item in options"
		                        :key="item.value"
		                        :label="item.label"
		                        :value="item.value">
		                </el-option>
		            </el-select>
		        </el-form-item>
				<el-form-item label="Amount" :label-width=formLabelWidth >
				    <el-input   v-model="amount" style="width: 221.4px;margin-left: 20px"></el-input>
				</el-form-item>
				<el-form-item>
				    <el-button type="primary" @click="buy(code, amount)" style="margin-left: 65px">BUY</el-button>
				    <el-button type="primary" @click="sell(code, amount)" style="margin-left: 180px">SELL</el-button>
				</el-form-item>
				
		        
		    </el-form>
		</el-dialog>
        
		<el-dialog :visible.sync="bs" style="width: 500px; margin: auto">
			<el-form :model="form" style="width: 100%">
				<el-form-item style="text-align: center">Successful purchase!</el-form-item>
			</el-form>
		</el-dialog>
		<el-dialog :visible.sync="bf" style="width: 500px; margin: auto">
			<el-form :model="form" style="width: 100%">
				<el-form-item style="text-align: center">Purchase failure!</el-form-item>
			</el-form>
		</el-dialog>
		<el-dialog :visible.sync="ss" style="width: 500px; margin: auto">
			<el-form :model="form" style="width: 100%">
				<el-form-item style="text-align: center">Successful sell!</el-form-item>
			</el-form>
		</el-dialog>
		<el-dialog :visible.sync="sf" style="width: 500px; margin: auto">
			<el-form :model="form" style="width: 100%">
				<el-form-item style="text-align: center">Failed to sell!</el-form-item>
			</el-form>
		</el-dialog>
		
    </div>

</template>

<script>
    import echarts from 'echarts'
    export default {
        name: "RealTime",
        data() {
            return {
                myChart:null,
                data: [],
				form: [],
				max: null,
				min: null,
                options:[
					{
						value: '000001',
						label: '000001'
					},
					{
						value: '000002',
						label: '000002'
					},
					{
						value: '000003',
						label: '000003'
					},
					{
						value: '000004',
						label: '000004'
					},
					{
						value: '000005',
						label: '000005'
					},
					{
						value: '000006',
						label: '000006'
					}
				],
				value:null,
				code:null,
				dialog:false,
				balance: 0,
				amount: null,
				formLabelWidth: '130px',
				charts_color: '#00da3c',
				bf:false,
				bs:false,
				sf:false,
				ss:false
            }
        },
        created() {
            
        },
        methods: {
			getbalance() {
				var url = '/api/getcount/';
				console.log(url)
				const _this = this;
				axios.get(url).then(
					function(data){
						console.log(data.data)
						if (data.data != null && data.data != "") {
							_this.balance = data.data
						}
					})
			},
			buy(code, amount) {
				console.log(code)
				console.log(amount)
				var url = '/api/buy/?code=' + code + '&num=' + amount;
				const _this = this;
				axios.get(url).then (
					function(data){
						if (data.data == 'fail') {
							_this.bf = true
						} else {
							_this.bs = true
						}
					})
				setTimeout(() =>{
				    this.getbalance();
				}, 4000);
			},
			sell(code, amount) {
				console.log(code)
				console.log(amount)
				var url = '/api/sale/?code=' + code + '&num=' + amount;
				const _this = this;
				axios.get(url).then (
					function(data){
						if (data.data == 'fail') {
							_this.sf = true
						} else {
							_this.ss = true
						}
					})
				setTimeout(() =>{
				    this.getbalance();
				}, 4000);
			},
			getcharts() {
				if (this.data[0][1] > this.data[this.data.length - 1][1]) {
					this.charts_color = '#00da3c';
				} else {
					this.charts_color = '#ec0000';
				}
				this.myChart = echarts.init(this.$refs.bar_dv);
				let option = {
				    grid:{
				        x:50,
				        y:50,
				        x2:50,
				        y2:60,
				        borderWidth:10
				    },
				    title: {
				        text: 'Real Time'
				    },
				    tooltip: {
				        trigger: 'axis',
						position: function (pt) {
						      return [pt[0], '10%'];
						}
				    },
				    xAxis: {
				        type:'time',
				        splitNumber:24
				    },
				    yAxis: {
						min: this.min - 0.5,
						max: this.max + 0.5,
				        splitLine: {
				            show: false
				        }
				    },
				    toolbox: {
				        left: 'center',
				        feature: {
				            dataZoom: {
				                yAxisIndex: 'none'
				            },
				            restore: {},
				            saveAsImage: {}
				        }
				    },
				    series: [
				        {
				            name: 'price',
				            type: 'line',
				            symbol: 'none',
							sampling: 'lttb',
							itemStyle: {
							        color: this.charts_color
							      },
							      // areaStyle: {
							      //   color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
							      //     {
							      //       offset: 0,
							      //       color: this.charts_color
							      //     },
							      //     {
							      //       offset: 1,
							      //       color: this.charts_color
							      //     }
							      //   ])
							      // },
				            data: this.data
				        }
				    ]
				};
					this.myChart.setOption(option);
			},
			query(value) {
				console.log(value)
				if (value != null) {
					var url = '/api/today/?code=' + value;
					console.log(url)
					const _this = this;
					axios.get(url).then(
						function(data){
							console.log(data.data)
							if (data.data != null && data.data != "") {
								_this.data = [];
								for(var i = 0;i<data.data.length;i++) {
									_this.data.push([data.data[i].时间, data.data[i].开盘]);
								}
								console.log(_this.data)
							}
						})
					var url = '/api/getmaxmin/?code=' + value;
					console.log(url)
					axios.get(url).then(function(data){
						if (data.data != null && data.data != "") {
							_this.max = data.data.max;
							_this.min = data.data.min;
						}
					})
				}
				setTimeout(() =>{
				    this.getcharts();
				}, 3000);
			}
        }
    }
</script>

<style scoped>

</style>