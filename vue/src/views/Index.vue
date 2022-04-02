<template>

    <el-container style="height: 754.4px;">
        <el-aside height="100%" width="200px" style="background-color: #343131;">
            <el-menu router :default-openeds="['1','0']" style="border:0px;background-color=#545c64;text-color=#fff;active-text-color=#ffd04b;">
				<el-submenu v-for="(item, i) in navList" :key= "i" :index="item.name">
					<template slot="title">
					  <i class="el-icon-s-home"></i>
					  <span> {{ item.navItem }}</span>
					</template>
					<el-menu-item v-for="(item2,i2) in item.children" :key="i2" :index="item2.name">
					        <template slot="title">
					          <i class="el-icon-s-platform"></i>
					          <span> {{ item2.navItem }}</span>
					        </template>
					
					      </el-menu-item>
				</el-submenu>
				<el-submenu v-for="(item, i) in list" :key= "i" :index="item.name">
					<template slot="title">
					  <i class="el-icon-s-tools"></i>
					  <span> {{ item.navItem }}</span>
					</template>
					<el-menu-item v-for="(item2,i2) in item.children" :key="i2" :index="item2.name">
					        <template slot="title">
					          <i class="el-icon-user-solid"></i>
					          <span> {{ item2.navItem }}</span>
					        </template>
					
					      </el-menu-item>
				</el-submenu>
            </el-menu>
        </el-aside>
        <el-main >
            <router-view></router-view>
        </el-main>

    </el-container>
</template>

<script>


    export default {
        name: "Index",
        data(){
			return{
				navList:[
					{
						name: '/stock',
						navItem: 'Stock',
						children: [
							{
								name: '/realtime',
								navItem: 'RealTime',
								children: []
							},
							{
								name: '/history',
								navItem: 'History',
								children: []
							}
						]
					}
				],
				list: [
					{
						name: '/setting',
						navItem: 'Setting',
						children: [
							{
								name: '/account',
								navItem: 'Account',
								children: []
							}
						]
					}
				]
          }
        },
        methods:{
            
        },
        created(){
			
        },
        mounted(){
        }

    }
</script>

<style>

</style>
<style>
    .el-menu-item.is-active {
        background-color: #ffffff !important;
    }
    .el-submenu__title:hover{
        background-color: #343131;
    }

    .el-carousel__item h3 {
        color: #475669;
        font-size: 14px;
        opacity: 0.75;
        line-height: 150px;
        margin: 0;
    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #99a9bf;
    }

</style>