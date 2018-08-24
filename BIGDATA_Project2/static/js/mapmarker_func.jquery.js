		//set up markers 
		var myMarkers = {"markers": [
				{"latitude": "37.5848936", "longitude":"127.026724", "icon": "static/img/map-marker.png"}
			]
		};
		
		//set up map options
		$(".map_contact").mapmarker({
			zoom	: 14,
			center	: '고려대학교 자연계캠퍼스',
			markers	: myMarkers
		});

