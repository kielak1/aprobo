/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(n){var e;(e=n&&n.fn&&n.fn.select2&&n.fn.select2.amd?n.fn.select2.amd:e).define("select2/i18n/ms",[],function(){return{errorLoading:function(){return"Keputusan tidak berjaya dimuatkan."},inputTooLong:function(n){return"Sila hapuskan "+(n.input.length-n.maximum)+" aksara"},inputTooShort:function(n){return"Sila masukkan "+(n.minimum-n.input.length)+" atau lebih aksara"},loadingMore:function(){return"Sedang memuatkan keputusan…"},maximumSelected:function(n){return"Anda hanya boleh memilih "+n.maximum+" pilihan"},noResults:function(){return"Tiada padanan yang ditemui"},searching:function(){return"Mencari…"},removeAllItems:function(){return"Keluarkan semua item"}}}),e.define,e.require},event=new CustomEvent("dal-language-loaded",{lang:"ms"});document.dispatchEvent(event);