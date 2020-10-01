# DISCLAIMER

_**This is a free copy of the depreciated product, offered several years ago at PTV Visum MarketPlace. 
This is not a standalone product, but Add-in for the PTV Visum software. 
The product is not mainained anymore. 
You can freely use it, or copy the code snippets to make your solutions. Though, there is no guarantee anymore.**_

***

# OptimalCountLocator_PTVVisum_AddIn
OCL tells you where to place counting locations in the transport model to get best results.  Our tool employs acknowledged optimization technique to specify set of optimal counting locations catching as much flow and as many OD pairs as possible. OCL is the optimization procedure wrapped in intuitive, user friendly interface, which can quickly find optimal solution even for complex networks.  User can define the budget (number of points that can be counted) and detectors which are already installed. It's also available to determine what kind of detectors we want to install: junction, link, directed link.  Additional technical parameter is algorithm depth, being number of paths between origin and destination that are taken into calculation process. We propose various strategies of optimization. In our opinion, and due to our tests, the most useful is mixed maximization of both OD pairs coverage and flow coverage, however you can choose to maximize only flow, or only OD pairs.  Running time depends on size of the network. On the average up-to-date PC it takes about 1 minute to download 300k paths (model for Kraków, Poland of ca. 350 zones), and then time of optimization itself depends on number of connectors and takes roughly 5s per detector.  To see results visually, you can import prepared .gpa file. Additionally you can use our flow bundle generator, where you can clearly see which flows are covered with your detection. For detailed results and statistics you can see report including OD coverage, flow coverage, keys of detected elements, calculation time, etc.  Screenshots and it will really help you in your work
