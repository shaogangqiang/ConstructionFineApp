package com.construction.fineapp

import android.graphics.Bitmap
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.construction.fineapp.ui.AnalysisScreen
import com.construction.fineapp.ui.CameraScreen
import com.construction.fineapp.ui.FineAmountScreen
import com.construction.fineapp.ui.HistoryScreen
import com.construction.fineapp.ui.ReceiptScreen
import com.construction.fineapp.ui.theme.FineAppTheme
import com.construction.fineapp.viewmodel.FineViewModel

class MainActivity : ComponentActivity() {
    private var currentBitmap: Bitmap? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            FineAppTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val viewModel: FineViewModel = viewModel()
                    val navController = rememberNavController()

                    val uiState by viewModel.uiState.collectAsState()

                    MainScreen(
                        viewModel = viewModel,
                        navController = navController,
                        setCurrentBitmap = { bitmap ->
                            currentBitmap = bitmap
                        },
                        getCurrentBitmap = { currentBitmap },
                        onShowHistory = { viewModel.toggleHistory() }
                    )
                }
            }
        }
    }
}

@Composable
fun MainScreen(
    viewModel: FineViewModel,
    navController: NavHostController,
    setCurrentBitmap: (Bitmap) -> Unit,
    getCurrentBitmap: () -> Bitmap?,
    onShowHistory: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()

    // Handle showHistory state changes
    LaunchedEffect(uiState.showHistory) {
        if (uiState.showHistory) {
            navController.navigate("history")
        }
    }

    NavHost(
        navController = navController,
        startDestination = "camera"
    ) {
        composable("camera") {
            CameraScreen(
                viewModel = viewModel,
                onImageCaptured = { bitmap ->
                    setCurrentBitmap(bitmap)
                    viewModel.captureImage(bitmap)
                    navController.navigate("amount")
                }
            )
        }

        composable("amount") {
            val bitmap = getCurrentBitmap() ?: run {
                navController.popBackStack()
                return@composable
            }
            FineAmountScreen(
                viewModel = viewModel,
                imageBitmap = bitmap,
                navController = navController,
                onBack = {
                    viewModel.clearCurrentImage()
                    navController.popBackStack()
                }
            )
        }

        composable("analysis") {
            val bitmap = getCurrentBitmap() ?: run {
                navController.popBackStack()
                return@composable
            }
            AnalysisScreen(
                viewModel = viewModel,
                imageBitmap = bitmap,
                navController = navController,
                onBack = {
                    navController.popBackStack()
                }
            )
        }

        composable("receipt") {
            val bitmap = getCurrentBitmap() ?: run {
                navController.popBackStack()
                return@composable
            }
            ReceiptScreen(
                viewModel = viewModel,
                imageBitmap = bitmap,
                navController = navController,
                onBack = {
                    navController.popBackStack()
                },
                context = androidx.compose.ui.platform.LocalContext.current
            )
        }

        composable("history") {
            HistoryScreen(
                viewModel = viewModel,
                navController = navController,
                onBack = {
                    viewModel.toggleHistory()
                    navController.popBackStack()
                }
            )
        }
    }
}

import androidx.compose.runtime.LaunchedEffect
