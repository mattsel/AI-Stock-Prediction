var stockSymbolsList = [
            ['Apple Inc. (AAPL)', 'AAPL'], ['Microsoft Corporation (MSFT)', 'MSFT'], ['Amazon.com Inc. (AMZN)', 'AMZN'], 
            ['Alphabet Inc. Class A (GOOGL)', 'GOOGL'], ['Alphabet Inc. Class C (GOOG)', 'GOOG'], ['Meta Platforms Inc. (FB)', 'FB'], ['Tesla Inc. (TSLA)', 'TSLA'], 
            ['Berkshire Hathaway Inc. Class B (BRK.B)', 'BRK.B'], ['Johnson & Johnson (JNJ)', 'JNJ'], ['JPMorgan Chase & Co. (JPM)', 'JPM'], ['Visa Inc. (V)', 'V'], 
            ['Procter & Gamble Co. (PG)', 'PG'], ['Netflix Inc. (NFLX)', 'NFLX'], ['Goldman Sachs Group Inc. (GS)', 'GS'], ['The Walt Disney Co. (DIS)', 'DIS'], 
            ['Cisco Systems Inc. (CSCO)', 'CSCO'], ['Comcast Corporation (CMCSA)', 'CMCSA'], ['International Business Machines Corp. (IBM)', 'IBM'], ['Verizon Communications Inc. (VZ)', 'VZ'], ['NVIDIA Corporation (NVDA)', 'NVDA'], 
            ['Exxon Mobil Corporation (XOM)', 'XOM'], ['AbbVie Inc. (ABBV)', 'ABBV'], ['Adobe Inc. (ADBE)', 'ADBE'], ['Accenture Plc Class A (ACN)', 'ACN'], 
            ['American Electric Power Company Inc. (AEP)', 'AEP'], ['AES Corporation (AES)', 'AES'], ['AFLAC Incorporated (AFL)', 'AFL'], ['American International Group Inc. (AIG)', 'AIG'], 
            ['Apartment Investment & Management Co. (AIV)', 'AIV'], ['Assurant Inc. (AIZ)', 'AIZ'], ['Arthur J. Gallagher & Co. (AJG)', 'AJG'], ['Allstate Corp. (ALL)', 'ALL'], ['Alaska Air Group Inc. (ALK)', 'ALK'], 
            ['Allegion plc (ALLE)', 'ALLE'], ['Alexion Pharmaceuticals Inc. (ALXN)', 'ALXN'], ['Amcor plc (AMCR)', 'AMCR'], ['Advanced Micro Devices Inc. (AMD)', 'AMD'], ['Ametek Inc. (AME)', 'AME'], 
            ['Amgen Inc. (AMGN)', 'AMGN'], ['Ameriprise Financial Inc. (AMP)', 'AMP'], ['American Tower Corp. (AMT)', 'AMT'], ['Arista Networks Inc. (ANET)', 'ANET'], ['ANSYS Inc. (ANSS)', 'ANSS'], 
            ['Aon plc Class A (AON)', 'AON'], ['A.O. Smith Corp. (AOS)', 'AOS'], ['APA Corporation (APA)', 'APA'], ['Air Products and Chemicals Inc. (APD)', 'APD'], 
            ['Amphenol Corporation Class A (APH)', 'APH'], ['Aptiv PLC (APTV)', 'APTV'], ['Alexandria Real Estate Equities Inc. (ARE)', 'ARE'], ['Align Technology Inc. (ALGN)', 'ALGN'], 
            ['Autoliv Inc. (ALV)', 'ALV'], ['Applied Materials Inc. (AMAT)', 'AMAT'], ['Archer-Daniels-Midland Co. (ADM)', 'ADM'], ['Truist Financial Corp. (TFC)', 'TFC'], 
            ['TransDigm Group Incorporated (TDG)', 'TDG'], ['The Travelers Companies Inc. (TRV)', 'TRV'], ['Tractor Supply Company (TSCO)', 'TSCO'], ['T. Rowe Price Group Inc. (TROW)', 'TROW'],
            ['Tyson Foods Inc. (TSN)', 'TSN'], ['Trane Technologies plc (TT)', 'TT'], ['Twitter Inc. (TWTR)', 'TWTR'], ['Textron Inc. (TXT)', 'TXT'], ['Tyler Technologies Inc. (TYL)', 'TYL'], 
            ['United Airlines Holdings Inc. (UAL)', 'UAL'], ['UDR Inc. (UDR)', 'UDR'], ['Universal Health Services Inc. Class B (UHS)', 'UHS'], ['Ulta Beauty Inc. (ULTA)', 'ULTA'], 
            ['UnitedHealth Group Incorporated (UNH)', 'UNH'], ['Unum Group (UNM)', 'UNM'], ['Union Pacific Corporation (UNP)', 'UNP'], ['United Parcel Service Inc. Class B (UPS)', 'UPS'],
            ['United Rentals Inc. (URI)', 'URI'], ['U.S. Bancorp (USB)', 'USB'], ['Valero Energy Corporation (VLO)', 'VLO'], ['Vulcan Materials Company (VMC)', 'VMC'], ['Vornado Realty Trust (VNO)', 'VNO'], 
            ['Verisk Analytics Inc. (VRSK)', 'VRSK'], ['VeriSign Inc. (VRSN)', 'VRSN'], ['Vertex Pharmaceuticals Incorporated (VRTX)', 'VRTX'], ['Ventas Inc. (VTR)', 'VTR'], ['Viatris Inc. (VTRS)', 'VTRS'],
            ['Westinghouse Air Brake Technologies Corporation (WAB)', 'WAB'], ['Waters Corporation (WAT)', 'WAT'], ['Walgreens Boots Alliance Inc. (WBA)', 'WBA'], ['Western Digital Corporation (WDC)', 'WDC'], 
            ['WEC Energy Group Inc. (WEC)', 'WEC'], ['Welltower Inc. (WELL)', 'WELL'], ['Wells Fargo & Company (WFC)', 'WFC'], ['Whirlpool Corporation (WHR)', 'WHR'], ['Willis Towers Watson Public Limited Company (WLTW)', 'WLTW'], 
            ['Waste Management Inc. (WM)', 'WM'], ['Williams Companies Inc. (WMB)', 'WMB'], ['Walmart Inc. (WMT)', 'WMT'], ['W. R. Berkley Corporation (WRB)', 'WRB'], ['WestRock Company (WRK)', 'WRK'], 
            ['West Pharmaceutical Services Inc. (WST)', 'WST'], ['Western Union Company (WU)', 'WU'], ['Weyerhaeuser Co. (WY)', 'WY'], ['Wynn Resorts Ltd. (WYNN)', 'WYNN'], ['Xcel Energy Inc. (XEL)', 'XEL'], 
            ['Xilinx Inc. (XLNX)', 'XLNX'], ['DENTSPLY SIRONA Inc. (XRAY)', 'XRAY'], ['Xerox Holdings Corporation (XRX)', 'XRX'], ['Xylem Inc. (XYL)', 'XYL'], ['Yum! Brands Inc. (YUM)', 'YUM'], 
            ['Zimmer Biomet Holdings Inc. (ZBH)', 'ZBH'], ['Zebra Technologies Corporation (ZBRA)', 'ZBRA'], ['Zions Bancorporation N.A. (ZION)', 'ZION'], ['Zoetis Inc. (ZTS)', 'ZTS']
        ];

        var stockSymbolsDatalist = document.getElementById("stock_symbols");
        var stockSymbolInput = document.getElementById("stock_symbol");

        // Function to generate list items based on data
        function generateList(data) {
            stockSymbolsDatalist.innerHTML = ""; // Clear previous list

            // Limit the number of options displayed
            var limit = Math.min(data.length, 4);

            for (var i = 0; i < limit; i++) {
                var option = document.createElement("option");
                option.value = data[i][1];
                option.textContent = data[i][0];
                stockSymbolsDatalist.appendChild(option);
            }
        }

        // Initial generation of list
        generateList(stockSymbolsList);

        // Event listener for search input
        stockSymbolInput.addEventListener("input", function() {
            var searchTerm = this.value.toLowerCase();
            var filteredData = stockSymbolsList.filter(function(item) {
                return item[0].toLowerCase().includes(searchTerm) || item[1].toLowerCase().includes(searchTerm);
            });
            generateList(filteredData);
        });

        // Event listener for selecting an option
        stockSymbolInput.addEventListener("change", function() {
            stockSymbolsDatalist.innerHTML = ""; // Clear the dropdown list
        });