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
const AGGREGATION_COLUMN_NUMBER = 7;//output_objectの列数


function analyze_vs_enemy_log(){
  let sheet_log = SPREADSHEET.getSheetByName(SHEETNAME_LOG);
  let sheet_output = SPREADSHEET.getSheetByName(SHEETNAME_VS_ANALYTICS);
  let data = fetchDataArray(sheet_log);
  let enemy_pokemon = extractDataArray(data, ENEMY_POKEMON_COLOMN_START, ENEMY_POKEMON_COLOMN_END, 1);
  let selected_pokemon = extractDataArray(data, ENEMY_SELECTED_POKEMON_COLOMN_START, ENEMY_SELECTED_POKEMON_COLOMN_END, 1);
  let first_pokemon = extractDataArray(data, ENEMY_SELECTED_POKEMON_COLOMN_START, ENEMY_SELECTED_POKEMON_COLOMN_START, 1);
  let unique_pokemon = make_unique_pokemon_data(enemy_pokemon);
  let output_object = [];//この中に1行の集計結果を格納する。

  //集計結果をoutput_objectに格納
  for (let pokemon in unique_pokemon){
    let pokemon_name = unique_pokemon[pokemon]
    output_object.push([
      pokemon_name,
      count_pokemon(enemy_pokemon, pokemon_name),
      count_pokemon(selected_pokemon, pokemon_name),
      count_pokemon(first_pokemon, pokemon_name),
      count_win(data, pokemon_name, ENEMY_POKEMON_COLOMN_START, ENEMY_POKEMON_COLOMN_END, WIN_COLUMN),
      count_win(data, pokemon_name, ENEMY_SELECTED_POKEMON_COLOMN_START, ENEMY_SELECTED_POKEMON_COLOMN_END, WIN_COLUMN),
      count_win(data, pokemon_name, ENEMY_SELECTED_POKEMON_COLOMN_START, ENEMY_SELECTED_POKEMON_COLOMN_START, WIN_COLUMN)
    ]);
  }

  //シートの既存情報を削除
  let clear_range = sheet_output.getRange(3,1, 1200, AGGREGATION_COLUMN_NUMBER);
  clear_range.clearContent();

  //シートに貼り付け
  let rows_num = unique_pokemon.length
  let pasted_range = sheet_output.getRange(3,1,rows_num, AGGREGATION_COLUMN_NUMBER)//行数、列数は1から開始。
  pasted_range.setValues(output_object)
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
 * @param {number} start_column_number - 取得を開始するカラム番号(A列は0)
 * @param {number} end_column_number - 取得を終了するカラム番号(A列は0)
 * @param {number} start_row_num - 取得を開始する行番号(1行目は0)。初期値を1としているので、デフォルトではインデックス名が削除される。
 * @return {Object} 
 */
function extractDataArray(array, start_column_number, end_column_number, start_row_num = 1){
  let data = array.slice(start_row_num).map(i => i.slice(start_column_number, end_column_number + 1));
  return data
}

/**
 * Objectからポケモン名が完全一致した要素の数を取得する。
 * 
 * @param {Object}
 * @param {string}
 * @return {number}
 */
function count_pokemon(array, pokemon_name){
  //pokemon_nameに一致した値のみをObjectに格納
  let found_pokemon = array.flat().filter((value) => value.match(pokemon_name));
  return found_pokemon.length
}

/**
 * Objectからユニークにポケモン名を取得する。
 * 
 * @param {Object} array
 * @return {Object} 要素がユニークなObject
 */
function make_unique_pokemon_data(array){
  let unique_pokemon = new Set(array.flat())
  return Array.from(unique_pokemon).filter(value => value.length != 0)
}

function count_win(
  array, 
  pokemon_name, 
  start_column_number, 
  end_column_number, 
  win_column_number, 
  start_row_num = 0
){
  let count_win = 0
  //検索範囲を指定。
  extract_array = extractDataArray(array, start_column_number, end_column_number, start_row_num)
  //1行ずつ処理。勝利であれば、count_winに加算。
  for (let i in extract_array){
    //行にポケモン名がなければ次の行へ。
    if (extract_array[i].flat().filter((value) => value.match(pokemon_name)).length == 0){
      continue;
    }

    let flag = array[i][win_column_number];
    if (flag == '〇'){
      count_win = count_win + 1;
    }
  }
  return count_win
}