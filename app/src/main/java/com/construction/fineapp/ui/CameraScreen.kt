package com.construction.fineapp.ui

import android.Manifest
import android.content.Context
import android.graphics.Bitmap
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.view.CameraController
import androidx.camera.view.LifecycleCameraController
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Camera
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.viewmodel.compose.viewModel
import com.google.accompanist.permissions.ExperimentalPermissionsApi
import com.google.accompanist.permissions.rememberPermissionState
import com.construction.fineapp.viewmodel.FineViewModel
import java.io.File
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

@OptIn(ExperimentalMaterial3Api::class, ExperimentalPermissionsApi::class)
@Composable
fun CameraScreen(
    viewModel: FineViewModel,
    onImageCaptured: (Bitmap) -> Unit
) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    val uiState by viewModel.uiState.collectAsState()

    val cameraPermission = rememberPermissionState(Manifest.permission.CAMERA)

    val cameraController = remember {
        LifecycleCameraController(context).apply {
            setEnabledUseCases(CameraController.IMAGE_CAPTURE)
        }
    }

    LaunchedEffect(Unit) {
        if (!cameraPermission.status.isGranted) {
            cameraPermission.launchPermissionRequest()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("拍照记录违规") },
                navigationIcon = {},
                actions = {
                    IconButton(onClick = { viewModel.toggleHistory() }) {
                        Icon(Icons.Default.History, "历史记录")
                    }
                }
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            if (cameraPermission.status.isGranted) {
                AndroidView(
                    factory = { ctx ->
                        androidx.camera.view.PreviewView(ctx).apply {
                            controller = cameraController
                            controller.bindToLifecycle(lifecycleOwner)
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )

                // 拍照按钮
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .padding(32.dp)
                ) {
                    FloatingActionButton(
                        onClick = {
                            val outputFile = File(
                                context.externalCacheDir,
                                "photo_${System.currentTimeMillis()}.jpg"
                            )
                            val outputFileOptions = ImageCapture.OutputFileOptions.Builder(outputFile).build()

                            cameraController.takePicture(
                                outputFileOptions,
                                Executors.newSingleThreadExecutor(),
                                object : ImageCapture.OnImageSavedCallback {
                                    override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                                        val bitmap = android.graphics.BitmapFactory.decodeFile(outputFile.absolutePath)
                                        onImageCaptured(bitmap)
                                    }

                                    override fun onError(exception: ImageCaptureException) {
                                        // Handle error
                                    }
                                }
                            )
                        },
                        modifier = Modifier.size(80.dp),
                        containerColor = MaterialTheme.colorScheme.primary
                    ) {
                        Icon(
                            Icons.Default.Camera,
                            "拍照",
                            modifier = Modifier.size(40.dp),
                            tint = Color.White
                        )
                    }
                }
            } else {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text("需要相机权限才能拍照")
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { cameraPermission.launchPermissionRequest() }) {
                        Text("授予权限")
                    }
                }
            }
        }
    }
}
