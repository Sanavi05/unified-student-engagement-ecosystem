const mongoose = require('mongoose');

const StudentProfileSchema = new mongoose.Schema(
  {
    userId: {
      type: String,
      required: true,
      unique: true,
      index: true,
    },
    demographics: {
      targetCountry: {
        type: String,
        default: null,
      },
      targetCourse: {
        type: String,
        default: null,
      },
      currentCGPA: {
        type: Number,
        default: null,
        min: 0,
        max: 4.0,
      },
    },
    financials: {
      estimatedCourseCost: {
        type: Number,
        default: 0,
      },
      userBudget: {
        type: Number,
        default: 0,
      },
      fundingGap: {
        type: Number,
        default: 0,
      },
    },
    engagementState: {
      copilotChatHistory: [
        {
          role: {
            type: String,
            enum: ['user', 'assistant'],
            required: true,
          },
          message: {
            type: String,
            required: true,
          },
          timestamp: {
            type: Date,
            default: Date.now,
          },
        },
      ],
      roiDashboardGenerated: {
        type: Boolean,
        default: false,
      },
      loanPreQualified: {
        type: Boolean,
        default: false,
      },
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model('StudentProfile', StudentProfileSchema);
