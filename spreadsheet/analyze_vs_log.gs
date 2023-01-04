const SPREADSHEET_ID ='12G4CLS_Ssbsgp0izcMmvefTuJnQwd6btBNjXikQrFAk';
const SHEETNAME_LOG = 'log';
const SHEETNAME_VS_ANALYTICS = '対戦分析_test';
const SHEETNAME_MY_TEAM_ANALYTICS = '自分チーム分析';
const SPREADSHEET = SpreadsheetApp.openById(SPREADSHEET_ID);
const ENEMY_POKEMON_COLOMN_START = 2;
const ENEMY_POKEMON_COLOMN_END = 7;
const ENEMY_SELECTED_POKEMON_COLOMN_START = 8;
const ENEMY_SELECTED_POKEMON_COLOMN_END = 10;
const WIN_COLUMN = 15;
const AGGREGATION_COLUMN_NUMBER = 7;//outputObjectの列数


function analyzeVSEnemyLog(){
  let sheetLog = SPREADSHEET.getSheetByName(SHEETNAME_LOG);
  let sheetOutput = SPREADSHEET.getSheetByName(SHEETNAME_VS_ANALYTICS);
  let data = fetchDataArray(sheetLog);
  let enemyPokemon = extractDataArray(data, ENEMY_POKEMON_COLOMN_START, ENEMY_POKEMON_COLOMN_END, 1);
  let selectedPokemon = extractDataArray(data, ENEMY_SELECTED_POKEMON_COLOMN_START, ENEMY_SELECTED_POKEMON_COLOMN_END, 1);
  let firstPokemon = extractDataArray(data, ENEMY_SELECTED_POKEMON_COLOMN_START, ENEMY_SELECTED_POKEMON_COLOMN_START, 1);
  let uniquePokemon = makeUniquePokemonData(enemyPokemon);
  let outputObject = [];//この中に1行の集計結果を格納する。

  //集計結果をoutputObjectに格納
  for (let pokemon in uniquePokemon){
    let pokemonName = uniquePokemon[pokemon]
    outputObject.push([
      pokemonName,
      countPokemon(enemyPokemon, pokemonName),
      countPokemon(selectedPokemon, pokemonName),
      countPokemon(firstPokemon, pokemonName),
      countWin(data, pokemonName, ENEMY_POKEMON_COLOMN_START, ENEMY_POKEMON_COLOMN_END, WIN_COLUMN),
      countWin(data, pokemonName, ENEMY_SELECTED_POKEMON_COLOMN_START, ENEMY_SELECTED_POKEMON_COLOMN_END, WIN_COLUMN),
      countWin(data, pokemonName, ENEMY_SELECTED_POKEMON_COLOMN_START, ENEMY_SELECTED_POKEMON_COLOMN_START, WIN_COLUMN)
    ]);
  }

  //シートの既存情報を削除
  let clearedRange = sheetOutput.getRange(3,1, 1200, AGGREGATION_COLUMN_NUMBER);
  clearedRange.clearContent();

  //シートに貼り付け
  let rowsNum = uniquePokemon.length
  let pastedRange = sheetOutput.getRange(3,1,rowsNum, AGGREGATION_COLUMN_NUMBER)//行数、列数は1から開始。
  pastedRange.setValues(outputObject)
}

/**
 * スプレッドシートからデータを取得する。
 * 
 * @param {Sheet} sheet - 特定のシート
 * @return {Object} 
 */
function fetchDataArray(sheet) {
  let data = sheet.getDataRange().getValues();
  return data
}

/**
 * Objectから必要なカラムのみの配列を取得する。
 * 
 * @param {Object} array
 * @param {number} startColumnNumber - 取得を開始するカラム番号(A列は0)
 * @param {number} endColumnNumber - 取得を終了するカラム番号(A列は0)
 * @param {number} startRowNum - 取得を開始する行番号(1行目は0)。初期値を1としているので、デフォルトではインデックス名が削除される。
 * @return {Object} 
 */
function extractDataArray(array, startColumnNumber, endColumnNumber, startRowNum = 1){
  let data = array.slice(startRowNum).map(i => i.slice(startColumnNumber, endColumnNumber + 1));
  return data
}

/**
 * Objectからポケモン名が完全一致した要素の数を取得する。
 * 
 * @param {Object}
 * @param {string}
 * @return {number}
 */
function countPokemon(array, pokemonName){
  //pokemonNameに一致した値のみをObjectに格納
  let foundPokemon = array.flat().filter((value) => value.match(pokemonName));
  return foundPokemon.length
}

/**
 * Objectからユニークにポケモン名を取得する。
 * 
 * @param {Object} array
 * @return {Object} 要素がユニークなObject
 */
function makeUniquePokemonData(array){
  let uniquePokemon = new Set(array.flat())
  return Array.from(uniquePokemon).filter(value => value.length != 0)
}

/**
 * Objectから、特定ポケモン名を含む場合の勝敗を取得する。
 * 
 * @param {Object} array
 * @param {string} pokemonName - 検索したいポケモン名
 * @param {number} startColumnNumber - 検索範囲の開始カラム番号(A列は0)
 * @param {number} endColumnNumber - 検索範囲の終了カラム番号(A列は0)
 * @param {number} winColumnNumber - 勝敗が記述されたカラム番号(A列は0)
 * @param {number} startRowNum - 取得を開始する行番号(1行目は0)。初期値を0としているので、デフォルトでは1行目が削除されない。
 * @return {number} 
 */
function countWin(
  array, 
  pokemonName, 
  startColumnNumber, 
  endColumnNumber, 
  winColumnNumber, 
  startRowNum = 0
){
  let wins = 0
  //検索範囲を指定。
  extractArray = extractDataArray(array, startColumnNumber, endColumnNumber, startRowNum)
  //1行ずつ処理。勝利であれば、countWinに加算。
  for (let i in extractArray){
    //行にポケモン名がなければ次の行へ。
    if (extractArray[i].flat().filter((value) => value.match(pokemonName)).length == 0){
      continue;
    }

    let flag = array[i][winColumnNumber];
    if (flag == '〇'){
      wins = wins + 1;
    }
  }
  return wins
}