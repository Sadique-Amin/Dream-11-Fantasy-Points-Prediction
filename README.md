# Dream Team Selection Optimization

This project aims to select an optimal cricket team based on various constraints and player attributes using linear programming with the `pulp` library.

## Overview

The `select_dream_team` function takes a DataFrame of players and their attributes, including player type, country, and fantasy score, and applies several constraints to select a team of 11 players that maximizes the total fantasy score.

## Constraints

The following constraints are implemented in the optimization model:

1. **Total Players Constraint**:
   - **Description**: The total number of players selected must equal 11.
   - **Implementation**: 
     ```python
     prob += pulp.lpSum([x[i] for i in range(num_players)]) == 11, "Total_players"
     ```

2. **Credit Limit Constraint**:
   - **Description**: The total credits used by the selected players must not exceed 100.
   - **Implementation**: 
     ```python
     prob += pulp.lpSum([players[i]["Credits"] * x[i] for i in range(num_players)]) <= 100, "Credit_limit"
     ```

3. **One Captain Constraint**:
   - **Description**: Exactly one player must be designated as the captain.
   - **Implementation**: 
     ```python
     prob += pulp.lpSum([c[i] for i in range(num_players)]) == 1, "One_captain"
     ```

4. **One Vice-Captain Constraint**:
   - **Description**: Exactly one player must be designated as the vice-captain.
   - **Implementation**: 
     ```python
     prob += pulp.lpSum([v[i] for i in range(num_players)]) == 1, "One_vice_captain"
     ```

5. **Captain and Vice-Captain Selection**:
   - **Description**: A player can only be designated as captain or vice-captain if they are selected in the team.
   - **Implementation**: 
     ```python
     for i in range(num_players):
         prob += c[i] <= x[i], f"Captain_if_selected_{i}"
         prob += v[i] <= x[i], f"ViceCaptain_if_selected_{i}"
         prob += c[i] + v[i] <= x[i], f"No_double_Designation_{i}"
     ```

6. **Player Type Constraints**:
   - **Description**: At least one player must be selected from each of the following categories: Wicket-Keeper (WK), Batsman (BAT), and All-Rounder (ALL). Bowlers (BOWL) are excluded from this requirement.
   - **Implementation**: 
     ```python
     for role in ["WK", "BAT", "ALL"]:
         prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == role]) >= 1, f"Role_{role}_constraint"
     ```

7. **Bowler Selection Constraint**:
   - **Description**: Exactly three bowlers must be selected in the team.
   - **Implementation**: 
     ```python
     prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == "BOWL"]) == 3, "Role_BOWL_constraint"
     ```

8. **Bowler from Each Team Constraint**:
   - **Description**: At least one bowler must be selected from each team represented in the player pool.
   - **Implementation**: 
     ```python
     for team in teams:
         prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Country"] == team and players[i]["Player Type"] == "BOWL"]) >= 1, f"At_least_one_bowler_from_{team}"
     ```

9. **Team Representation Constraint**:
   - **Description**: At least five players must be selected from each team, except for teams that are in the restricted countries list.
   - **Implementation**: 
     ```python
     for team in teams:
         if team not in restricted_countries:
             prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Country"] == team]) >= 5, f"Team_{team}_constraint"
     ```
## Additional Constraints

10. **Pitch Conditions**:
    - **Description**: The selection of players should consider the pitch report. A batting-friendly pitch demands more batters, while a bowling-friendly pitch emphasizes bowlers.
    - **Implementation**: 
      ```python
      if pitch_condition == "batting-friendly":
          prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == "BAT"]) >= num_batters, "Batting_friendly_pitch"
      elif pitch_condition == "bowling-friendly":
          prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == "BOWL"]) >= num_bowlers, "Bowling_friendly_pitch"
      ```

11. **Weather Conditions**:
    - **Description**: Weather conditions can affect gameplay. Rain can reduce overs, impacting players' performance.
    - **Implementation**: 
      ```python
      if weather_condition == "rain":
          prob += pulp.lpSum([x[i] for i in range(num_players)]) <= reduced_overs_limit, "Weather_rain_constraint"
      ```

12. **T20 Fantasy Cricket Strategy**:
    - **Description**: 
        1. Pick power hitters who can score quickly.
        2. Focus on bowlers who excel in death overs.
        3. Select all-rounders for extra points.
    - **Implementation**: 
      ```python
      prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == "BAT" and players[i]["Power Hitter"]]) >= num_power_hitters, "Power_Hitters_constraint"
      prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == "BOWL" and players[i]["Death Overs Specialist"]]) >= num_death_overs_bowlers, "Death_Overs_Bowlers_constraint"
      prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == "ALL"]) >= num_all_rounders, "All_Rounders_constraint"
      ```

13. **Opponent Analysis**:
    - **Description**: Evaluate how players perform against specific opponents. This can influence the selection of batters and bowlers.
    - **Implementation**: 
      ```python
      for opponent in opponents:
          prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Opponent"] == opponent and players[i]["Player Type"] == "BAT"]) >= expected_runs[opponent], f"Expected_runs_against_{opponent}"
          prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Opponent"] == opponent and players[i]["Player Type"] == "BOWL"]) >= expected_wickets[opponent], f"Expected_wickets_against_{opponent}"
      ```

14. **Bias in Selection**:
    - **Description**: Create a bias in the selection of the number of batters and bowlers from each team based on expected runs scored and wickets taken.
    - **Mathematical Implementation**: 
      Let $R_i$ be the expected runs scored by team $i$ and $W_i$ be the expected wickets taken by team $i$. The selection bias can be represented as:

      $$
      \text{Bias}_{BAT} = \frac{R_i}{R_{total}} \times \text{Total\_Batters} + \text{Weight}_{AR} \times \text{Total\_AllRounders}
      $$

      $$
      \text{Bias}_{BOWL} = \frac{W_i}{W_{total}} \times \text{Total\_Bowlers} + \text{Weight}_{AR} \times \text{Total\_AllRounders}
      $$

      The selection of batters and bowlers from each team can be influenced by these biases, ensuring that the team composition reflects the expected performance based on historical data.
      - **Implementation**: 
      ```python
      for team in teams:
          prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Country"] == team and players[i]["Player Type"] == "BAT"]) >= Bias_BAT[team], f"Bias_BAT_{team}"
          prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Country"] == team and players[i]["Player Type"] == "BOWL"]) >= Bias_BOWL[team], f"Bias_BOWL_{team}"
      ```

  15. **Top Order vs. Bottom Order Batsmen**:
    - **Description**: The selection process should prioritize top-order batsmen if historical data indicates they are likely to perform well. Consequently, the algorithm should limit the number of bottom-order batsmen selected for batting roles.
    - **Implementation**: 
      ```python
      # Define the maximum number of bottom-order batsmen allowed
      max_bottom_order = 2  # Example value, adjust based on your strategy

      # Add the constraint to the optimization problem
      prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == "BAT" and players[i]["Order"] == "Bottom"]) <= max_bottom_order, "Max_Bottom_Order_Batsmen"
      ```




## Conclusion

This optimization model ensures a balanced selection of players while adhering to various constraints, maximizing the overall fantasy score for the selected cricket team.

## Importance of Values for the Optimization Algorithm

In the optimization algorithm for selecting the cricket team, several key values are essential to ensure a balanced and effective team composition:

1. **Expected Runs Scored by Each Team $R_i$**:
   - The expected runs scored by each team provide a crucial metric for evaluating the potential performance of batters. This value helps in determining which players are likely to contribute significantly to the team's total score, allowing the algorithm to prioritize high-scoring batters.

2. **Expected Wickets Taken by Each Team $W_i$**:
   - Similarly, the expected wickets taken by each team are vital for assessing the effectiveness of bowlers. This metric informs the selection process by highlighting bowlers who are likely to take crucial wickets, thereby impacting the opposition's scoring ability.

3. **Performance of All-Rounders**:
   - All-rounders play a unique role in the team, contributing both with bat and ball. Their performance metrics are weighted more heavily in the selection process, as they provide additional flexibility and scoring potential. By evaluating their contributions in both disciplines, the algorithm can prioritize all-rounders who can significantly impact the game.

4. **Weather Conditions**:
   - Weather details are critical for predicting the nature of the innings. For instance, if conditions suggest that the innings will be short (e.g., due to rain), the algorithm can adjust the selection strategy to favor aggressive batters who can score quickly in limited overs. This adaptability is essential for maximizing the team's performance under varying conditions.

5. **Top Order vs. Bottom Order Batsmen**:
   - The algorithm also considers the expected performance of top-order batsmen. If historical data indicates that the top order is likely to perform well, the selection process may deprioritize bottom-order batsmen for batting roles. This ensures that the team is composed of players who are most likely to contribute to the score, optimizing the overall batting lineup.

By integrating these values into the optimization algorithm, the selection process becomes more data-driven and strategic, ultimately leading to a more competitive cricket team.

## Predicting Team Performance

In addition to optimizing team selection based on various constraints, we can also predict the potential performance of teams with a certain probability of scoring points. This predictive capability allows us to identify teams that may have a higher risk but also a higher potential for performance.

### Mathematical Foundation

Let:
- $P(T)$ be the probability of team $T$ scoring a certain number of points.
- $E(R_i)$ be the expected runs scored by team $i$.
- $E(W_i)$ be the expected wickets taken by team $i$.
- $R_{threshold}$ be the threshold score we want to predict.

The probability of a team scoring above a certain threshold can be modeled as:

$$
P(T) = P(E(R_i) > R_{threshold}) \times P(E(W_i) > W_{threshold})
$$

Where:
- $P(E(R_i) > R_{threshold})$ is the probability that the expected runs scored by the team exceeds the threshold.
- $P(E(W_i) > W_{threshold})$ is the probability that the expected wickets taken by the team exceeds the threshold.

### Risk Assessment

To assess the risk associated with selecting a high-performance team, we can define a risk factor $R_f$ based on the variance of the expected performance metrics:

$$
R_f = \sigma^2(E(R_i)) + \sigma^2(E(W_i))
$$

Where:
- $\sigma^2(E(R_i))$ is the variance of the expected runs scored.
- $\sigma^2(E(W_i))$ is the variance of the expected wickets taken.

A higher risk factor indicates a more volatile performance, which may lead to higher rewards but also greater uncertainty.

By integrating these predictive models into the optimization algorithm, we can make more informed decisions about team selection, balancing the potential for high scores against the associated risks.

