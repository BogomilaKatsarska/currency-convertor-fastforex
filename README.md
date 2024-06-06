Currency Convertor - CLI application for Appolica <br>
• Use Python, Node.js or Kotlin.<br>
• The application must accept a command line argument for the date in format '2024-12-31'.<br>
• The application must be able to process multiple conversions.<br>
• The application must continuously validate all inputs until a correct one is submitted. Мonetary values should be constrained to two decimal places. Currencies must be in ISO 4217 three letter currency code format.<br>
• The application must be case-insensitive.<br>
• The application must cache the exchange rates for each requested base currency. Subsequent conversions with this base currency should use the cached data, instead of calling the API.<br>
• Each successful conversion must be saved in a json file with the provided format.<br>
• The application must be terminated by typing 'END' on any input.<br>
• The application must load the api_key for Fast Forex from a config.json file which must be ignored by the version control.<br>
• The executable must be named CurrencyConversion.<br>
