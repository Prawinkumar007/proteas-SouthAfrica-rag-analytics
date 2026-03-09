import pandas as pd
import glob
import os

def get_phase(over):
    """Determine match phase based on over number."""
    if over < 6:
        return "powerplay"
    elif over < 15:
        return "middle"
    else:
        return "death"

def process_data(raw_dir, output_file):
    all_files = glob.glob(os.path.join(raw_dir, "*.csv"))
    if not all_files:
        print(f"Error: No CSV files found in {raw_dir}")
        print("Please download Cricsheet ball-by-ball CSV data and place it in data/raw/")
        return

    processed_events = []
    
    # Track statistics
    total_matches = len(all_files)
    total_events = 0
    start_date = None
    end_date = None

    for f in all_files:
        try:
            df = pd.read_csv(f)
            
            # Check if South Africa is involved
            # Cricsheet CSVs typically have 'batting_team' or 'bowling_team'
            # Note: Cricsheet structure can vary, but common columns are:
            # match_id, season, start_date, venue, innings, ball, batting_team, bowling_team, striker, non_striker, bowler, runs_off_bat, extras, wides, noballs, byes, legbyes, penalty, wicket_type, player_dismissed, other_wicket_type, other_player_dismissed
            
            if 'South Africa' not in df['batting_team'].unique() and 'South Africa' not in df['bowling_team'].unique():
                continue
            
            # Determine opponent and match details
            teams = df['batting_team'].unique()
            opponent = [t for t in teams if t != 'South Africa'][0] if len(teams) > 1 else "Unknown"
            venue = df['venue'].iloc[0]
            start_date_val = df['start_date'].iloc[0]
            year = str(start_date_val)[:4]
            
            # Update date range
            if start_date is None or start_date_val < start_date:
                start_date = start_date_val
            if end_date is None or start_date_val > end_date:
                end_date = start_date_val

            # Group by over to create "over events" or process ball-by-ball?
            # User requirement: "Convert each over into a rich text string"
            # So we group by innings and over (integer part of 'ball')
            df['over_num'] = df['ball'].apply(lambda x: int(x))
            
            grouped = df.groupby(['innings', 'over_num'])
            
            for (innings, over), group in grouped:
                batting_team = group['batting_team'].iloc[0]
                bowling_team = group['bowling_team'].iloc[0]
                
                # Filter for events involving SA (either batting or bowling)
                # But usually we want all events in a SA match for context
                
                runs = group['runs_off_bat'].sum()
                extras = group['extras'].sum()
                wickets = group['player_dismissed'].count()
                
                # Cricsheet doesn't always have "format" in the ball-by-ball CSV, 
                # but we can infer or it might be in a separate info file.
                # For now, let's assume it's in the data or default to "International"
                match_format = "International" # Placeholder if not found
                
                phase = get_phase(over)
                
                # Match situation: team score for wickets
                # Needs cumulative count - requires iterating through the match
                # Let's simplify and use the state at the end of the over
                # To do this properly, we'd need to track state across overs in the loop
            
            # Re-processing with cumulative state tracking
            current_score = 0
            current_wickets = 0
            for (innings_idx, over_idx), group in grouped:
                batting_team = group['batting_team'].iloc[0]
                bowling_team = group['bowling_team'].iloc[0]
                
                runs = group['runs_off_bat'].sum()
                extras = group['extras'].sum()
                total_runs_in_over = runs + extras
                wickets_in_over = group['player_dismissed'].count()
                
                current_score += total_runs_in_over
                current_wickets += wickets_in_over
                
                bowler = group['bowler'].iloc[0]
                batsmen = ", ".join(group['striker'].unique())
                
                # Reset score/wickets for new innings
                if innings_idx > 1 and over_idx == 0:
                    current_score = total_runs_in_over
                    current_wickets = wickets_in_over

                text = (f"SA vs {opponent}, {match_format}, {venue}, {year}, "
                        f"Over {over_idx} ({phase}), "
                        f"{bowler} bowled to {batsmen}, {runs} runs scored, "
                        f"{wickets_in_over} wickets, extras: {extras}. "
                        f"Match situation: {batting_team} {current_score} for {current_wickets}")
                
                processed_events.append({
                    'text': text,
                    'opponent': opponent,
                    'format': match_format,
                    'phase': phase,
                    'year': int(year),
                    'venue': venue,
                    'bowler': bowler,
                    'batsmen': batsmen
                })
                total_events += 1

        except Exception as e:
            print(f"Error processing {f}: {e}")

    if processed_events:
        pd.DataFrame(processed_events).to_csv(output_file, index=False)
        print("--- Ingestion Summary ---")
        print(f"Total Matches Processed: {total_matches}")
        print(f"Total Events Generated: {total_events}")
        print(f"Date Range: {start_date} to {end_date}")
        print(f"Saved to: {output_file}")
    else:
        print("No events processed. Check if South Africa matches are present.")

if __name__ == "__main__":
    process_data("data/raw", "data/processed_events.csv")
