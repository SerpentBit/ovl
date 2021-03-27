Feature: Ambient Vision

  Scenario Outline: Iteration timing
    Given an ambient vision pipeline
    And a specific timing configuration <timing_configuration>
    When Iterating the pipeline
    Then Detections should match the timings
    Examples:
      | timing_configuration |
      | 1                    |
      | 2
      | 0.5                  |