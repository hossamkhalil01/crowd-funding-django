"use strict";

var app = angular.module("app", ["slick", "ui.sortable"]);

app.controller('sortableController', function ($scope) {
  var tmpList = [];
  
  var originalScreens = [
    { title: 'Espresso shot' },
    { title: 'Water' },
    { title: 'Foam' },
    { title: 'Milk' },
    { title: 'Whipped cream' },
    { title: 'Syrop' },
    { title: 'Sugar' },
    { title: 'Ice' }
  ];
  $scope.images = [];
  for(var i = 0; i<15; ++i){
    $scope.images.push({'idx':i});
  }
  $scope.sourceScreens = originalScreens.slice();
  $scope.selectedScreens = [{ title: 'Espresso shot' }];
  
  
  
  $scope.sortingLog = [];
  
  $scope.sortableOptions = {
    connectWith: ".connected-apps-container",
    stop: function (e, ui) {
      // if the element is removed from the first container
      if ($(e.target).hasClass('first') &&
          ui.item.sortable.droptarget &&
          e.target != ui.item.sortable.droptarget[0]) {
        // clone the original model to restore the removed item
        $scope.sourceScreens = originalScreens.slice();
      }
    }
  };
  
});