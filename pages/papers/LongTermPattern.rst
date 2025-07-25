.. title: Long-Term Pattern Formation and Maintenance for Battery-Powered Robots
.. slug: LongTermPattern/2017
.. date: 1970-01-01 00:00:00 UTC
.. tags:
.. link: http://www.mistlab.ca/papers/LongTermPattern/2017/
.. description: Supplementary material

.. raw:: html

	<style type="text/css">
		.tg  {border-collapse:collapse;border-spacing:0;}
		.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
		.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
		.tg .tg-yw4l{vertical-align:top}

		td { vertical-align: top; font-size: 12px; font-style: italic;}
		body {line-height: 22px;}
	</style>

	<h2>Supplementary material </h2>

	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title" id="known_region_coverage">Known region coverage</h3>
		</div>
		<div class="panel-body">
			<h3 id="simulation_setup">Simulation setup</h3>

			<div style="width: 100%; overflow: hidden;">
    			<div style="width: 65%; float: left;">
					<p align="justify">
						The simulations are performed using a multi-physics simulator <a href="http://www.argos-sim.info/">ARGoS</a> while the control software is written in a domain specific language <a href="the.swarming.buzz">Buzz</a>. Furthermore, control software, i.e. the behavior is implemented through a well defined state machine (explained in the full paper). In every simulation shown below, all robots start with the state <i>Idle</i>, after which the pattern formation algorithm initiates the deployment process.
						<br/>
						Depending on robots current state, its battery is discharged in a different rate, as shown in the table bellow. For example, if a robot is moving towards its target position its battery is discharged with 1 A, since when it is moving it uses 0.8 A, and when its idle (on-board computers and sensors) it uses 0.2 A. When a robot is <i>Joined</i> to the formation (meaning that it holds a required position) the discharge current is such that it simulates heavy processing by on-board computers, i.e. performing a designated task (e.g. network coverage, sensing, etc.). The battery model simulates a LiPo-kind of non-linear discharging and recharging for a single celled battery with 4.2 V, and a reduced capacity of 200 mAh, to keep the duration of simulations reasonable.
					</p>

					<br/>
					<table class="tg" align="center" style="line-height: normal;">
					  <tr>
					    <th class="tg-031e">ACC idle (supporting on-board electronics)</th>
					    <th class="tg-yw4l">ACC driving</th>
					    <th class="tg-yw4l">ACC in formation</th>
					    <th class="tg-yw4l">Battery capacity</th>
					  </tr>
					  <tr>
					    <td class="tg-yw4l" align="center">0.2 A</td>
					    <td class="tg-yw4l" align="center">0.8 A</td>
					    <td class="tg-yw4l" align="center">1.2 A</td>
					    <td class="tg-yw4l" align="center">200 mAh</td>
					  </tr>
					  <tr>
					  	<td colspan=4 style="border: none; line-height:normal; font-size:12px;">* ACC: average current consumption</td>
					  </tr>
					</table>
					<br/>
					<p align="justify">
						We have made an empirical observation that 8000 simulation steps are sufficient to demonstrate the stability of the system, so that each robot gets one recharging cycle. With simulation step set to <i>0.1 S</i>, the run--time of each simulation translates to 8 minutes in the real world.
						<br/>
						The simulation was performed using four different patterns (formations) which were selected with the following concerns a) depth of the tree (which translates to number of position exchanges for a robot to reach the power station and to the maximal number of possible position exchanges at any given moment) and b) the position and number of direct successors from the charging station (which relates to the number of robots competing to recharge).
					</p>
    			</div>
    			<div style="float: right; width: 30%" class="panel panel-default panel-body">
					<b>Content:</b>
					<ul style="list-style-type:circle">
					  <li><a href="#known_region_coverage">Known region coverage</a></li>
					  	<ul>
					  		<li><a href="#simulation_setup">Simulation setup</a></li>
					  		<li><a href="#patterns">Patterns a,b,c,d</a></li>
					  	</ul>
					  <li><a href="#unknown_100">Unknown region coverage - simulations</a></li>
					  	<ul>
					  		<li><a href="#simulations_100">Large multi--robot team: 120 members</a></li>
					  		<li><a href="#scaling">Scaling comparison</a></li>
					  	</ul>
					  <li><a href="#khepera">Experiments with Khepera IV</a></li>
					  	<ul>
					  		<li><a href="#known_6">Known region (6 robots)</a></li>
					  		<li><a href="#unknown_6">Unknown region (6 robots)</a></li>
					  		<li><a href="#unknown_8">Unknown region (8 robots)</a></li>
					  	</ul>
					</ul>
    			</div>
			</div>
		</div>
	</div>

		<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title">Pattern formation - ARGoS simulations</h3>
		</div>
		<div class="panel-body">
			<h3 id="patterns">Pattern a)</h3>
			<table style="width: 210px; margin-left: auto; margin-right: auto; float: right;">
				<tbody>
					<tr>
						<td align="center" style="padding: 10px;"><img src="pattern-a.png" class="img-responsive" alt="Pattern a" width="200px"/></td>
					</tr>
					<tr>
						<td style="padding: 10px;">Pattern with highest tree depth (8). Robots are in the line formation. Black node represents the charging station.</td>
					</tr>
				</tbody>
			</table>

			<p align="justify">
				The pattern formation <i>a</i> shown by the figure on the right has 9 positions which robots need to take. Its shape is in a form of a chain, in which each robot has only one successor (with exception to leaf positions). The depth of the tree representing this pattern is 8, meaning, that the furthest robot (one in the leaf position) needs to perform 8 position exchanges in order to reach a charging station. This topology allows for at most three simultaneous position exchanges (since each exchange involves three robots).
				<br/>
				Given the previously described parameters, the pattern formation was stable with at most 6 robots, effectively reducing the depth to 5. The formation is considered stable if during the simulation run-time, none of the robots are fully discharged (and doesn't show a tendency to do so).

				<br/>
				For each robot, if its successor has a lower state of charge (SoC), they exchange positions. Therefore, in accordance to the proposed algorithm robots continuously compare their SoCs, and if necessary, engage in the position exchange procedure. In this way, robots with the most SoC are pushed toward the edges, while the robots with the least SoC are attracted towards a charging station. To see how this effects the overall continuity, i.e. stability of the pattern itself (number of robots present in the formation), consider the bottom left figure. For pattern formation <i>a</i> it shows that the 40 - 100% of robots are at any given point at the exact position of the established pattern while the rest of them are  exchanging positions. This means that mostly 1 to 4 robots are moving, while the rest are staying still in the formation, simulating data processing; operating under assumption that when a robot is joined in the formation, it does some useful work.

				<br/>
				The right most figure bellow shows that on average more than 80% robots are in the pattern, meaning that on average only 1 or 2 are not in the pattern nor in a nearby position (a robot can be in a nearby position still performing the given task, however just slightly moved away to make space for its replacement, i.e. its successor traveling down the tree to the charging station). Furthermore, figures bellow show the percentage of robots available for performing a given task, and state of charge throughout the simulation. No robots are fully discharged.
			</p>


			<table style="width: 100%; margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td><img src="pattern-a-stop.png" class="img-responsive" alt="Pattern a stop" height="400px"/></td>
						<td><img src="pattern-a-processing.png" class="img-responsive" alt="Pattern a processing" height="400px"/></td>
						<td align="center"><img src="pattern-a-soc.png" class="img-responsive" alt="Pattern a SOC" height="400px"/></td>

					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="left">Left part of the figure shows the percentage of robots in the formation <i>a</i> which are holding their position in the pattern during 8000 simulation steps. Right part shows the percentage of robots in the state <i>Joined</i> in robots are able to perform a given task.</td>
						<td style="padding: 2px;" align="center">State of charge for each robot in the pattern a. The most robots it can support is 6 out of 9.</td>
					</tr>
				</tbody>
			</table>

			<hr/>

			<h3>Pattern b)</h3>
			<table style="width: 210px; margin-left: auto; margin-right: auto; float: right;">
				<tbody>
					<tr>
						<td align="center" style="padding: 10px;"><img src="pattern-b.png" class="img-responsive" alt="Pattern b" width="150px"/></td>
					</tr>
					<tr>
						<td style="padding: 10px;" align="center">Pattern b)</td>
					</tr>
				</tbody>
			</table>


			<p align="justify">
				Pattern <i>b</i> shown on the side figure has the total depth of 3, meaning that robots at leaf positions need 3 position changes to reach the charging station. The topology of the tree representing this formation allows for only two position exchanges at most. If the robot at the root of the tree and its successor are engaged in the position exchange process, robots in both the left and right side of the sub-tree cannot engage in position exchange since their successor is busy. Consequently, this makes this formation the one with the highest average percentage of robots which are at any given moment joined in the formation and performing their task, i.e between 80 - 100%, averaging on 90% of robots.
			</p>

			<table style="width: 100%; margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td><img src="pattern-b-stop.png" class="img-responsive" alt="Pattern b stop" height="400px"/></td>
						<td><img src="pattern-b-processing.png" class="img-responsive" alt="Pattern b processing" height="400px"/></td>
						<td align="center"><img src="pattern-b-soc.png" class="img-responsive" alt="Pattern b SOC" height="400px"/></td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="left">Left part of the figure shows the percentage of robots in the formation <i>b</i> which are holding their position in the pattern during 8000 simulation steps. Right part shows the percentage of robots in the state <i>Joined</i> in robots are able to perform a given task.</td>
						<td style="padding: 2px;" align="center">State of charge for each robot in the pattern b. At most, it was stable with 7 robots.</td>
					</tr>
				</tbody>
			</table>

			<hr/>

			<h3>Pattern c)</h3>
			<table style="width: 210px; margin-left: auto; margin-right: auto; float: right;">
				<tbody>
					<tr>
						<td align="center" style="padding: 10px;"><img src="pattern-c.png" class="img-responsive" alt="Pattern c" width="210px"/></td>
					</tr>
					<tr>
						<td style="padding: 10px;" align="center">Pattern c)</td>
					</tr>
				</tbody>
			</table>

			<p align="justify">
				Given its depth and number of direct branches from the root, pattern formation <i>c</i> shown on the side figure, is the most interesting one since it has a good representation of properties of all other patterns. It is similar to the pattern formation <i>a</i>, however the charging station is located at the middle of the tree, which splits its depth to 4, meaning that robots at leaf positions need to make at most four position exchanges in order to reach the charging station. Also, since the root has two successors, at any given moment two robots are competing to access the charging station.
				<br/>
				As shown in the figures bellow, 60 - 80% of robots are at the exact position of the established pattern while the remaining ones  are engaged in position exchange. One can notice that mostly 2 to 4 robots are moving simultaneously while the remaining ones keep still, joined in the formation. Also, the (middle) figure shows that on average 80% robots are joined in the pattern performing a given task. Since this formation was stable with all 9 robots, in absolute terms this means that on average 1 or 2 robots are not in the pattern or at their nearby positions (i.e. are traveling towards their predecessors to exchange positions).
			</p>

			<table style="width: 100%; margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td><img src="pattern-c-stop.png" class="img-responsive" alt="Pattern c stop" height="400px"/></td>
						<td><img src="pattern-c-processing.png" class="img-responsive" alt="Pattern c processing" height="400px"/></td>
						<td align="center"><img src="pattern-c-soc.png" class="img-responsive" alt="Pattern c SOC" height="400px"/></td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="left">Left part of the figure shows the percentage of robots in the formation <i>c</i> which are holding their position in the pattern during 8000 simulation steps. Right part shows the percentage of robots in the state <i>Joined</i> in robots are able to perform a given task.</td>
						<td style="padding: 2px;" align="center">State of charge for each robot in the pattern c.</td>
					</tr>
				</tbody>
			</table>

			<hr/>

			<h3>Pattern d)</h3>
			<table style="width: 210px; margin-left: auto; margin-right: auto; float: right;">
				<tbody>
					<tr>
						<td align="center" style="padding: 10px;"><img src="pattern-d.png" class="img-responsive" alt="Pattern d" width="210px"/></td>
					</tr>
					<tr>
						<td style="padding: 10px;" align="center">Pattern d)</td>
					</tr>
				</tbody>
			</table>

			<p align="justify">
				The side figure shows the pattern <i>d</i> with the lowest depth and a root with most direct successors. In this pattern four robots are competing to get to the charging station at once, and each robot located in the leaf position needs only two position exchanges to reach the charging station.
				<br/>
				At any given moment, this pattern formation allows for four pairs of robots to exchange positions. The consequence of this is shown in the most left figure bellow. The left part shows that between 60 - 100% of robots are joined in the formation, while on average 80% of the robots are performing their task. Given the fact that this formation involved 9 robots, this means that mostly 3 of the robots were not present in the pattern, however only 1 or 2 of these did not perform their task (i.e. were not in their nearby position).
				<br/>
				At most, pattern <i>d</i> could support 9 robots as shown in the most right figure bellow. None of the robots fully discharge and SoC does not drop bellow 50%.
			</p>

			<table style="width: 100%; margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td><img src="pattern-d-stop.png" class="img-responsive" alt="Pattern d stop" height="400px"/></td>
						<td><img src="pattern-d-processing.png" class="img-responsive" alt="Pattern d processing" height="400px"/></td>
						<td align="center"><img src="pattern-d-soc.png" class="img-responsive" alt="Pattern d SOC" height="400px"/></td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="center">Left part of the figure shows the percentage of robots in the formation d which are holding their position in the pattern during 8000 simulation steps. Right part shows the percentage of robots in the state <i>Joined</i> in robots are able to perform a given task.</td>
						<td style="padding: 2px;" align="center">State of charge for each robot in the pattern <i>d</i>.</td>
					</tr>
				</tbody>
			</table>

		</div>
	</div>

	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title" id="unknown_100">Unknown region coverage - ARGoS simulations</h3>
		</div>
		<div class="panel-body">
			<h3 id="simulations_100">Simulating a large multi--robot team: 100 robots and 20 charging stations</h3>

			<p align="justify">
				This subsection shows how previous observations can be used to scale up in order to build a large multi--robot team capable of long term autonomy. Using our approach fully presented in the paper, we are able to successfully deploy a large multi--robot team with 120 robots, of which there are 20 charging stations.
				<br/>
				The simulation setup is the same as in previous section, however, since it takes a longer time for a multi--robot team to be deployed and for each robot to go through a recharging cycle, therefore we changed only two parameters: a) increased the battery capacity to <i>300 mAh</i> and b) increased simulation time to 12000 steps, which corresponds to 20 minutes in real world.
			</p>

			<table style="margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td style="vertical-align:middle" align="center">
							<iframe width="560" height="315" src="https://www.youtube.com/embed/Vv66kcK8ot4" frameborder="0" allowfullscreen></iframe>
						</td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="center">ARGoS simulation of 100 robots and 20 charging stations. None of the team members get fully discharged in 12000 simulation steps. The video is sped up 6 times.</td>
					</tr>
				</tbody>
			</table>

			<p align="justify">
				In order to cover an unknown region we use a potential function for the deployment of robots to spread the multi--robot team to the most surface area. Figures bellow, along with videos illustrate a simulated region of 10x10 meters in which we deploy 100 robots with a coverage area of <i>1 m</i>. The target area to cover is a circular area with a radius of <i>8 m</i>. The darker circle represents this area, while the smaller circles represent robots with individual cover radii.
				<br/>
				It can be noticed that the coverage never reaches 100%, as shown in the most left figure bellow. It shows the coverage percentage of the target area in any given moment of the simulation with a sampling rate of <i>0.1 Hz</i>. Around step 100 the deployment is complete, and then some of the robots proceed to recharge. The highest coverage is 98.05%, the lowest 86.87% and on average it is 91.35%.
			</p>

			<table style="width: 95%; margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td style="vertical-align:middle"><img src="coverage-percentage.png" class="img-responsive" alt="Coverage percentage 100 robots" width="550px"/></td>
						<td style="vertical-align:middle" align="center"><img src="coverage-percentage-2.png" class="img-responsive" alt="Available robots percentage for 100 member multi--robot team" width="550px"/></td>
						<td><img src="forest-100-soc.png" class="img-responsive" alt="Forest 100 members SOC" width="600px"/></td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="left">Left figure shows the surface coverage of an area with 8 m radius (shown in a figure below). The right figure shows the percentage of performing useful work (ones not exchanging positions)</td>
						<td style="padding: 2px;" align="left">State of charge of all robots during the simulation. None of the robots get fully discharged</td>
					</tr>
				</tbody>
			</table>

			<br/>

			<table style="width: 70%; margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td style="vertical-align:middle" align="center"><img src="coverage-forest-area-100.png" class="img-responsive" alt="Coverage area 100 robots" width="300px"/></td>
						<td style="vertical-align:middle" align="center"><img src="argos-ss-100.png" class="img-responsive" alt="ARGoS 100 robots, 20 charging stations" width="400px"/></td>
					</tr>
					<tr>
						<td style="padding: 2px; " align="center">Robots each covering area of one meter squared, while the target area to cover is represented by a blue circle.</td>
						<td style="padding: 2px;" align="center">Generated balanced forest used for recharging.</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>

	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title" id="scaling">Unknown region coverage - ARGoS simulations, Scaling comparison </h3>
		</div>
		<div class="panel-body">
			<h3>Scaling our approach, comparison between warms of various sizes</h3>

			<p align="justify">
				Figures bellow show how our approach scales for unknown region coverage with respect to: a) tree generation, b) covered surface, c) state of charge and d) available robots for performing useful work.
			</p>

			<table style="margin-left: auto; margin-right: auto;">
				<tbody>
					<tr><td colspan=3 style="font-size: 16px; border-bottom: 1px solid #ccc; padding-top: 15px;"><b>Generated tree:</b></td></tr>
					<tr><td colspan=3 style="font-size: 14px; text-style: normal">
						<p align="justify">
							From the standpoint of generated trees, algorithm scales well and produces balanced trees. With 25 robots, the smallest tree only had three members, while for the largest trees hat 8 members. Furthermore, none of the generated trees have a depth larger than 2, which is one of the most important points of the algorithm, as stated in discussion related for the known region coverage.
						</p>
					</td></tr>
					<tr>
						<td style="vertical-align:middle" align="center"><img src="25-swarm.png" class="img-responsive" alt="ARGoS 25" width="300px"/></td>
						<td style="vertical-align:middle" align="center"><img src="50-swarm.png" class="img-responsive" alt="ARGoS 50" width="300px"/></td>
						<td style="vertical-align:middle" align="center"><img src="75-swarm.png" class="img-responsive" alt="ARGoS 75" width="300px"/></td>
					</tr>
					<tr>
						<td style="padding: 2px;" align="center">Generated forest for 25 robots, 7 charging stations</td>
						<td style="padding: 2px;" align="center">Generated forest for 50 robots, 10 charging stations</td>
						<td style="padding: 2px;" align="center">Generated forest for 70 robots, 15 charging stations</td>
					</tr>
					<tr><td colspan=3 style="font-size: 16px; border-bottom: 1px solid #ccc; padding-top: 15px;"><b>Area coverage:</b></td></tr>
					<tr><td colspan=3 style="font-size: 14px; text-style: normal">
						<p align="justify">
							Depending on the number of robots, the surface to cover had a radius of 4.5 m, 6 m and 7.5 m respectfully for 25, 50 and 75 robots. Figures bellow show the state of area coverage while the multi--robot team is fully deployed, just before generating a forest.
						</p>
					</td></tr>
					<tr>
						<td style="vertical-align:middle" align="center"><img src="cov-25-area.png" class="img-responsive" alt="Area 25" width="300px"/></td>
						<td style="vertical-align:middle" align="center"><img src="cov-50-area.png" class="img-responsive" alt="Area 50" width="300px"/></td>
						<td style="vertical-align:middle" align="center"><img src="cov-75-area.png" class="img-responsive" alt="Area 75" width="300px"/></td>
					</tr>
					<tr>
						<td style="padding: 2px;" align="center">Area covered by 25 robots, radius of 4.5 m</td>
						<td style="padding: 2px;" align="center">Area covered by 50 robots, radius of 6 m</td>
						<td style="padding: 2px;" align="center">Area covered by 75 robots, radius of 7.5 m</td>
					</tr>
					<tr><td colspan=3 style="font-size: 16px; border-bottom: 1px solid #ccc; padding-top: 15px;"><b>Percentage of covered area:</b></td></tr>
					<tr><td colspan=3 style="font-size: 14px; text-style: normal">
						<p align="justify">
							One can notice that the least area coverage is made with 25 robots. Although the area surface is reduced, still it is to large for 25 robots thus averaging with only 77.54% coverage. Furthermore, regarding to oscillations in coverage, the multi--robot team with 75 robots was the most stable one, because in relative terms the smaller amount of robots can be charged at once.
						</p>
					</td></tr>
					<tr>
						<td style="vertical-align:middle" align="center"><img src="cov-25-perc.png" class="img-responsive" alt="Coverage 25" width="300px"/></td>
						<td style="vertical-align:middle" align="center"><img src="cov-50-perc.png" class="img-responsive" alt="Coverage 50" width="300px"/></td>
						<td style="vertical-align:middle" align="center"><img src="cov-75-perc.png" class="img-responsive" alt="Coverage 75" width="300px"/></td>
					</tr>
					<tr>
						<td style="padding: 2px;" align="center">Percentage of covered area with 25 robots (min: 73.34%, max: 91.56%, avg: 82.92%)</td>
						<td style="padding: 2px;" align="center">Percentage of covered area with 50 robots (min: 80.01%, max: 95.34%, avg: 88.27%)</td>
						<td style="padding: 2px;" align="center">Percentage of covered area with 75 robots (min: 62.38%, max: 92.32%, avg: 87.08%)</td>
					</tr>
					<tr><td colspan=3 style="font-size: 16px; border-bottom: 1px solid #ccc; padding-top: 15px;"><b>State of charge:</b></td></tr>
					<tr><td colspan=3 style="font-size: 14px; text-style: normal">
						<p align="justify">
							In none of the simulations does any of the robots get discharged, however, one can notice that with less robots the average minimal charge of each robot never drops below 75%, while in the case of 50 and 75 robots this was never bellow 60% (except for one robot which was about to get recharged, before simulation ended).
						</p>
					</td></tr>
					<tr>
						<td style="vertical-align:middle" align="center"><img src="soc-25.png" class="img-responsive" alt="SOC 25" width="350px"/></td>
						<td style="vertical-align:middle" align="center"><img src="soc-50.png" class="img-responsive" alt="SOC 50" width="350px"/></td>
						<td style="vertical-align:middle" align="center"><img src="soc-75.png" class="img-responsive" alt="SOC 75" width="350px"/></td>
					</tr>
					<tr>
						<td style="padding: 2px;" align="center">State of charge for a team with 25 members. </td>
						<td style="padding: 2px;" align="center">State of charge for a team with 50 members. </td>
						<td style="padding: 2px;" align="center">State of charge for a team with 75 members. </td>
					</tr>
					<tr><td colspan=3 style="font-size: 16px; border-bottom: 1px solid #ccc; padding-top: 15px;"><b>Robots available for performing useful work:</b></td></tr>
					<tr><td colspan=3 style="font-size: 14px; text-style: normal">
						<p align="justify">
							Number of robots available for useful work (i.e. in state <i>Joined</i>) also differs by the number of team members. With 25 robots it was the lowest, while for the team of 50 and 75 robots it was similar. This is due to the fact that with a smaller team of 25 robots, the average size of the tree was smaller thus allowing robots to go and recharge more frequently (which is also evident in the associated state of charge figure).
						</p>
					</td></tr>
					<tr>
						<td style="vertical-align:middle" align="center"><img src="25-proc.png" class="img-responsive" alt="Working robots 25" width="350px"/></td>
						<td style="vertical-align:middle" align="center"><img src="50-proc.png" class="img-responsive" alt="Working robots 50" width="350px"/></td>
						<td style="vertical-align:middle" align="center"><img src="75-proc.png" class="img-responsive" alt="Working robots 75" width="350px"/></td>
					</tr>
					<tr>
						<td style="padding: 2px;" align="center">Percentage out of 25 robots available for work (min: 56.00%, max: 80.00%, avg: 67.58%)</td>
						<td style="padding: 2px;" align="center">Percentage out of 50 robots available for work (min: 70.00%, max: 86.00%, avg: 79.15%)</td>
						<td style="padding: 2px;" align="center">Percentage out of 75 robots available for work (min: 73.33%, max: 84.00%, avg: 79.39%)</td>
					</tr>
				</tbody>
			</table>

			<br/>
		</div>
	</div>

	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title" id="khepera">Real world experiments using Khepera IV</h3>
		</div>
		<div class="panel-body">
			<h3 id="known_6">Known region coverage: 1 charging station, 5 robots, star formation</h3>

			<p align="justify">
				The video bellow shows the experiment of covering a known region with five robots and one charging station. The given pattern is a star formation. Initially, robots are in applying for a label within the recharging tree. The default behavior of a robot without the label is moving around the central point, i.e. the charging station. Once a charging station joins the formation, the first robot is applies for a label, and gets approved. After this, the next one applies, and the process continues until all robots have their labels. Once this is complete, the recharging process starts. The recharging itself is simulated with a fixed amount of time, demonstrating a proof of concept.
			</p>

			<table style="margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td style="vertical-align:middle">
							<iframe width="560" height="315" src="https://www.youtube.com/embed/PEUV4UuxQ9k" frameborder="0" allowfullscreen></iframe>
						</td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="center">Star formation with 5 robots and 1 charging station.</td>
					</tr>
				</tbody>
			</table>

			<br/>

			<p align="justify">
				The current design of Khepera IV which is used in this experiment uses a LiPo battery which allows for five hours of autonomy and requires about the same time to fully recharge. In order make experiments more efficient and less time consuming, we simulate battery discharge of <i>6%</i> per minute by software allowing for autonomy of <i>1000 S</i> (16.6 minutes) making it 18 times faster than reality. When a robot docks to the charging station and we have a solid contact, we simulate a fast battery replacement taking <i>1.5 S</i>, which translates to roughly half a minute in the real time.
			</p>

			<table style="width: 80%; margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td style="vertical-align:middle"><img src="known-processing.png" class="img-responsive" alt="Joining state" width="550px"/></td>
						<td><img src="known-soc.png" class="img-responsive" alt="Known region experiment SOC" width="560px"/></td>
					</tr>
					<tr>
						<td style="padding: 2px;" align="center">Percentage of robots in the state Joined.</td>
						<td style="padding: 2px;" align="center">Simulated state of charge for each Khepera used in the experiment.</td>
					</tr>
				</tbody>
			</table>

			<hr/>

			<h3 id="unknown_6">Unknown region coverage: 1 charging station, 5 robots</h3>

			<p align="justify">
				The video bellow shows the experiment of covering an unknown region with five robots and one charging station. Robots are initially expanding using the Lennard-Jones potential, while the charging station holds its position. Once the area is covered, our algorithms generate a tree and calculate the best position for a charging station (with respect to tree depth). Then, the charging station moves to this position and the recharging process starts. The robot which initially held the position which is now taken by a charging station, moves to a position of a robot next in line for recharging.
			</p>

			<table style="margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td style="vertical-align:middle">
							<iframe width="560" height="315" src="https://www.youtube.com/embed/9L5955yon1A" frameborder="0" allowfullscreen></iframe>
						</td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="center">Unknown region coverage with 5 robots and 1 charging station.</td>
					</tr>
				</tbody>
			</table>

			<p align="justify">
				For this experiment we slowed down the simulated battery discharge to <i>2%</i> per minute, while the recharging time remained the same. This difference is visible in the state of charge figure, and when compared to the previous one (known region coverage), one can notice that the levels do not drop bellow <i>80%</i>. This becomes even more interesting, when compared to the next experiment with two charging stations, where the parameters are the same but the state of charge never drops bellow <i>85%</i>, since the charging stations have less load.
				<br/>
				The figures bellow show the covered area when the multi--robot team is fully deployed (i.e. just before the recharging process starts), along with the state of charge.
			</p>

			<table style="width: 95%; margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td align="center"><img src="coverage-tree-area.png" class="img-responsive" alt="Coverage tree" width="280px"/></td>
						<td style="vertical-align:middle"><img src="coverage-tree-percentage.png" class="img-responsive" alt="Coverage percentage tree" width="280px"/></td>
						<td style="vertical-align:middle"><img src="tree-soc.png" class="img-responsive" alt="SOC Tree" height="400px"/></td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="left">Left figure shows the area covered while the multi--robot team is fully deployed, while the middle figure shows area coverage percentage throughout the experiment. On average the coverage is 73.87% (min: 63.42%, max: 86.02%).</td>
						<td style="padding: 2px;" align="center">Simulated state of charge for each robot (only one charging station).</td>
					</tr>
				</tbody>
			</table>

			<hr/>

			<h3 id="unknown_8">Unknown region coverage: 2 charging stations, 6 robots</h3>

			<p align="justify">
				The video bellow shows the experiment of covering an unknown region with five robots and two charging stations. Similarly as in the previous experiment, robots are using the Lennard-Jones potential to cover the region as much as possible. Charging stations are holding their position during this state. After robots expanded as much as possible, the forest is generated using our algorithms, and since there are two charging stations, forest consists of two trees. Then, for each tree, the best position for a charging station is calculated after which charging stations proceed to take their positions using only local positioning and neighbor communication to navigate. After this, for each tree the recharging process starts independently and continuous until the end of the experiment.
			</p>

			<table style="margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td style="vertical-align:middle">
							<iframe width="560" height="315" src="https://www.youtube.com/embed/V9s5qOgDHA8" frameborder="0" allowfullscreen></iframe>
						</td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="center">Unknown region coverage 5 robots and 2 charging stations.</td>
					</tr>
				</tbody>
			</table>

			<p align="justify">
				Although these can be considered optimistic, the state of charge figure bellow shows that the battery levels are always above <i>80%</i> of charge, leaving plenty of room for much more conservative charging and discharging time assumptions. Furthermore, in this setup, there are only three robots per a single charging station which makes for much more frequent recharging than in the previous case (with five robots per a single charging station).
			</p>

			<table style="width: 95%; margin-left: auto; margin-right: auto;">
				<tbody>
					<tr>
						<td><img src="exp-forest-coverage.png" class="img-responsive" alt="Forest coverage" width="280px"/></td>
						<td style="vertical-align:middle"><img src="exp-forest-coverage2.png" class="img-responsive" alt="Forest coverage percentage" width="280px"/></td>
						<td><img src="forest-soc.png" class="img-responsive" alt="Forest SOC" height="400px"/></td>
					</tr>
					<tr>
						<td colspan="2" style="padding: 2px;" align="left">Left figure shows the area covered while the multi--robot team is fully deployed, while the middle figure shows area coverage percentage throughout the experiment. On average the coverage is 74.20% (min: 60.17.42%, max: 87.96%). </td>
						<td style="padding: 2px;" align="center">Simulated state of charge for each robot (two charging stations, three robots per each).</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>

	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title" id="known_region_coverage">C++ code</h3>
		</div>
		<div class="panel-body">
			<div style="width: 100%; overflow: hidden;">
					<div style="width: 65%; float: left;">
					<p align="justify">
						<a href="BoostGraphCentrality_GraphOperations.cpp">BoostGraphCentrality_GraphOperations.cpp</a>
					</p>
			</div>
		</div>
	</div>
